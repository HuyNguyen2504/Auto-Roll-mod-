"""
Mouse & Region Saver - B1 popup (Name + Description)
Hotkeys:
 - Ctrl+B : save coordinate (coords table)
 - Ctrl+P : two-step region saving:
     * press once -> save origin point (x1,y1) and enter "waiting" state
     * press second time -> compute width/height, open popup (Name + Description). If OK -> save region.
 - Esc or Ctrl+B while waiting -> cancel region creation.

Implementation notes:
 - Uses `keyboard` for global hotkeys.
 - SQLite used for persistent storage.
"""

import sys
import threading
import time
import sqlite3
import pyautogui
import keyboard

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QMessageBox, QDialog, QLineEdit, QTextEdit,
    QFormLayout, QDialogButtonBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

# ----------------------------
# Database manager
# ----------------------------
class Database:
    def __init__(self, db_name="coords.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        q_coords = """
        CREATE TABLE IF NOT EXISTS coords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            x INTEGER,
            y INTEGER
        );
        """
        q_regions = """
        CREATE TABLE IF NOT EXISTS regions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            x1 INTEGER,
            y1 INTEGER,
            width INTEGER,
            height INTEGER
        );
        """
        self.conn.execute(q_coords)
        self.conn.execute(q_regions)
        self.conn.commit()

    # coords
    def add_coord(self, name, x, y):
        q = "INSERT INTO coords (name, x, y) VALUES (?, ?, ?)"
        cur = self.conn.execute(q, (name, x, y))
        self.conn.commit()
        return cur.lastrowid

    def delete_coord(self, row_id):
        q = "DELETE FROM coords WHERE id = ?"
        self.conn.execute(q, (row_id,))
        self.conn.commit()

    def update_coord(self, row_id, name, x, y):
        q = "UPDATE coords SET name = ?, x = ?, y = ? WHERE id = ?"
        self.conn.execute(q, (name, x, y, row_id))
        self.conn.commit()

    def get_all_coords(self):
        q = "SELECT id, name, x, y FROM coords ORDER BY id ASC"
        return self.conn.execute(q).fetchall()

    # regions
    def add_region(self, name, description, x1, y1, width, height):
        q = """INSERT INTO regions (name, description, x1, y1, width, height)
               VALUES (?, ?, ?, ?, ?, ?)"""
        cur = self.conn.execute(q, (name, description, x1, y1, width, height))
        self.conn.commit()
        return cur.lastrowid

    def delete_region(self, row_id):
        q = "DELETE FROM regions WHERE id = ?"
        self.conn.execute(q, (row_id,))
        self.conn.commit()

    def update_region(self, row_id, name, description, x1, y1, width, height):
        q = """UPDATE regions SET name=?, description=?, x1=?, y1=?, width=?, height=? WHERE id=?"""
        self.conn.execute(q, (name, description, x1, y1, width, height, row_id))
        self.conn.commit()

    def get_all_regions(self):
        q = "SELECT id, name, description, x1, y1, width, height FROM regions ORDER BY id ASC"
        return self.conn.execute(q).fetchall()

# ----------------------------
# B1 Popup (Name + Description)
# ----------------------------
class RegionDialog(QDialog):
    def __init__(self, default_name="", default_description="", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Region Info (Name & Description)")
        self.setModal(True)

        self.name_edit = QLineEdit(default_name)
        self.desc_edit = QTextEdit(default_description)
        self.desc_edit.setFixedHeight(90)

        form = QFormLayout()
        form.addRow("Name:", self.name_edit)
        form.addRow("Description:", self.desc_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def get_data(self):
        return self.name_edit.text().strip(), self.desc_edit.toPlainText().strip()

# ----------------------------
# Hotkey listener thread
# ----------------------------
class HotkeyListener(threading.Thread):
    def __init__(self, app_obj):
        super().__init__()
        self.daemon = True
        self.app_obj = app_obj
        self.running = True

    def run(self):
        try:
            keyboard.add_hotkey("ctrl+b", lambda: QTimer.singleShot(0, self.app_obj._hotkey_coord))
            keyboard.add_hotkey("ctrl+p", lambda: QTimer.singleShot(0, self.app_obj._hotkey_region))
            keyboard.add_hotkey("esc",    lambda: QTimer.singleShot(0, self.app_obj._hotkey_escape))
        except Exception as e:
            print("Failed to register hotkeys:", e)
            return
        while self.running:
            time.sleep(0.2)

    def stop(self):
        self.running = False
        try:
            keyboard.unhook_all_hotkeys()
        except Exception:
            pass

# ----------------------------
# Main app
# ----------------------------
class MouseRegionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()

        self.setWindowTitle("Mouse & Region Saver — B1 Popup")
        self.setGeometry(100, 100, 900, 600)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # region creation state
        self.region_stage = 0
        self.region_temp_point = None
        self.region_stage_time = None

        self._suppress_coords_changed = False
        self._suppress_regions_changed = False

        self.coord_label = None
        self.status_label = None
        self.coord_table = None
        self.region_table = None

        self._build_ui()
        self.load_all()
        self._start_tracker()

        self.hk_thread = HotkeyListener(self)
        self.hk_thread.start()

        self.stage_timer = QTimer(self)
        self.stage_timer.timeout.connect(self._check_region_timeout)
        self.stage_timer.start(500)

    # ---------------- UI ----------------
    def _build_ui(self):
        main = QVBoxLayout(self)

        top_group = QGroupBox("Mouse Position & Status")
        top_layout = QHBoxLayout(top_group)
        self.coord_label = QLabel("X: -, Y: -")
        self.coord_label.setFont(QFont("Courier New", 18, QFont.Bold))
        self.coord_label.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(self.coord_label)

        self.status_label = QLabel("Status: Idle")
        self.status_label.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(self.status_label)
        main.addWidget(top_group)

        center_layout = QHBoxLayout()

        # coords
        coords_group = QGroupBox("Coords (Ctrl+B)")
        coords_layout = QVBoxLayout(coords_group)
        self.coord_table = QTableWidget(0, 4)
        self.coord_table.setHorizontalHeaderLabels(["ID", "Name", "X", "Y"])
        self.coord_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.coord_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.coord_table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
        self.coord_table.itemChanged.connect(self._on_coords_item_changed)
        coords_layout.addWidget(self.coord_table)

        btn_del_coord = QPushButton("Delete Selected Coord")
        btn_del_coord.clicked.connect(self._delete_selected_coord)
        coords_layout.addWidget(btn_del_coord)
        center_layout.addWidget(coords_group, 1)

        # regions
        regions_group = QGroupBox("Regions (Ctrl+P)")
        regions_layout = QVBoxLayout(regions_group)
        self.region_table = QTableWidget(0, 7)
        self.region_table.setHorizontalHeaderLabels(["ID", "Name", "Description", "X1", "Y1", "Width", "Height"])
        self.region_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.region_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.region_table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
        self.region_table.itemChanged.connect(self._on_regions_item_changed)
        regions_layout.addWidget(self.region_table)

        btn_del_region = QPushButton("Delete Selected Region")
        btn_del_region.clicked.connect(self._delete_selected_region)
        regions_layout.addWidget(btn_del_region)
        center_layout.addWidget(regions_group, 1)

        main.addLayout(center_layout)

        instr = QLabel("Instr: Ctrl+B → save coord. Ctrl+P → save region (2 presses). ESC to cancel region creation.")
        instr.setAlignment(Qt.AlignCenter)
        main.addWidget(instr)

    # ---------------- Tracker ----------------
    def _start_tracker(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_mouse_pos)
        self.timer.start(30)

    def _update_mouse_pos(self):
        try:
            x, y = pyautogui.position()
            self.coord_label.setText(f"X: {x}   Y: {y}")
        except Exception:
            self.coord_label.setText("X: -, Y: -")

    # ---------------- Load DB ----------------
    def load_all(self):
        self._load_coords()
        self._load_regions()

    def _load_coords(self):
        rows = self.db.get_all_coords()
        self._suppress_coords_changed = True
        self.coord_table.setRowCount(0)
        for (rid, name, x, y) in rows:
            self._insert_coord_row(rid, name, x, y)
        self._suppress_coords_changed = False

    def _load_regions(self):
        rows = self.db.get_all_regions()
        self._suppress_regions_changed = True
        self.region_table.setRowCount(0)
        for (rid, name, desc, x1, y1, w, h) in rows:
            self._insert_region_row(rid, name, desc, x1, y1, w, h)
        self._suppress_regions_changed = False

    # ---------------- Insert helpers ----------------
    def _insert_coord_row(self, rid, name, x, y):
        r = self.coord_table.rowCount()
        self.coord_table.insertRow(r)
        id_item = QTableWidgetItem(str(rid))
        id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
        self.coord_table.setItem(r, 0, id_item)
        self.coord_table.setItem(r, 1, QTableWidgetItem(name))
        self.coord_table.setItem(r, 2, QTableWidgetItem(str(x)))
        self.coord_table.setItem(r, 3, QTableWidgetItem(str(y)))

    def _insert_region_row(self, rid, name, desc, x1, y1, width, height):
        r = self.region_table.rowCount()
        self.region_table.insertRow(r)
        id_item = QTableWidgetItem(str(rid))
        id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
        self.region_table.setItem(r, 0, id_item)
        self.region_table.setItem(r, 1, QTableWidgetItem(name))
        self.region_table.setItem(r, 2, QTableWidgetItem(desc))
        self.region_table.setItem(r, 3, QTableWidgetItem(str(x1)))
        self.region_table.setItem(r, 4, QTableWidgetItem(str(y1)))
        self.region_table.setItem(r, 5, QTableWidgetItem(str(width)))
        self.region_table.setItem(r, 6, QTableWidgetItem(str(height)))

    # ---------------- Hotkey handlers ----------------
    def _hotkey_coord(self):
        if self.region_stage == 1:
            self._cancel_region("Cancelled: Ctrl+B pressed while waiting for region point2")
            return
        try:
            x, y = pyautogui.position()
        except Exception:
            QMessageBox.warning(self, "Error", "Cannot read mouse position.")
            return
        name = f"coord_{int(time.time())}"
        rid = self.db.add_coord(name, x, y)
        self._suppress_coords_changed = True
        self._insert_coord_row(rid, name, x, y)
        self._suppress_coords_changed = False
        self.status_label.setText(f"Status: Coord saved ID {rid}")

    def _hotkey_region(self):
        try:
            x, y = pyautogui.position()
        except Exception:
            QMessageBox.warning(self, "Error", "Cannot read mouse position.")
            return

        if self.region_stage == 0:
            self.region_stage = 1
            self.region_temp_point = (x, y)
            self.region_stage_time = time.time()
            self.status_label.setText(f"Status: Region point1 saved ({x},{y}). Press Ctrl+P again or ESC/Ctrl+B to cancel.")
            return
        elif self.region_stage == 1:
            x1, y1 = self.region_temp_point
            x2, y2 = x, y
            width = abs(x2 - x1)
            height = abs(y2 - y1)

            dlg = RegionDialog(default_name=f"region_{int(time.time())}", default_description=f"w={width}, h={height}", parent=self)
            res = dlg.exec_()
            if res == QDialog.Accepted:
                name, desc = dlg.get_data()
                if not name:
                    QMessageBox.warning(self, "Invalid", "Region name is required. Region not saved.")
                    self._reset_region_state()
                    return
                rid = self.db.add_region(name, desc, x1, y1, width, height)
                self._suppress_regions_changed = True
                self._insert_region_row(rid, name, desc, x1, y1, width, height)
                self._suppress_regions_changed = False
                self.status_label.setText(f"Status: Region '{name}' saved (ID {rid}).")
            else:
                self.status_label.setText("Status: Region creation canceled by user.")
            self._reset_region_state()

    def _hotkey_escape(self):
        if self.region_stage == 1:
            self._cancel_region("Cancelled: ESC pressed")

    # ---------------- Region helpers ----------------
    def _cancel_region(self, message="Cancelled"):
        self._reset_region_state()
        self.status_label.setText(f"Status: {message}")

    def _reset_region_state(self):
        self.region_stage = 0
        self.region_temp_point = None
        self.region_stage_time = None

    def _check_region_timeout(self):
        if self.region_stage == 1 and self.region_stage_time:
            if time.time() - self.region_stage_time > 30:
                self._cancel_region("Cancelled: region creation timed out (30s)")

    # ---------------- Table edit handlers ----------------
    def _on_coords_item_changed(self, item):
        if self._suppress_coords_changed:
            return
        row = item.row()
        id_item = self.coord_table.item(row, 0)
        if not id_item:
            return
        try:
            rid = int(id_item.text())
            name = self.coord_table.item(row, 1).text()
            x = int(self.coord_table.item(row, 2).text())
            y = int(self.coord_table.item(row, 3).text())
        except Exception:
            QMessageBox.warning(self, "Invalid", "Coord fields invalid (X,Y must be integers). Reverting.")
            self._load_coords()
            return
        self.db.update_coord(rid, name, x, y)
        self.status_label.setText(f"Status: Coord ID {rid} updated.")

    def _on_regions_item_changed(self, item):
        if self._suppress_regions_changed:
            return
        row = item.row()
        id_item = self.region_table.item(row, 0)
        if not id_item:
            return
        try:
            rid = int(id_item.text())
            name = self.region_table.item(row, 1).text()
            desc = self.region_table.item(row, 2).text()
            x1 = int(self.region_table.item(row, 3).text())
            y1 = int(self.region_table.item(row, 4).text())
            width = int(self.region_table.item(row, 5).text())
            height = int(self.region_table.item(row, 6).text())
        except Exception:
            QMessageBox.warning(self, "Invalid", "Region fields invalid (must be integers). Reverting.")
            self._load_regions()
            return
        self.db.update_region(rid, name, desc, x1, y1, width, height)
        self.status_label.setText(f"Status: Region ID {rid} updated.")

    # ---------------- Delete handlers ----------------
    def _delete_selected_coord(self):
        row = self.coord_table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Select Row", "Please select a coord row to delete.")
            return
        rid = int(self.coord_table.item(row, 0).text())
        if QMessageBox.question(self, "Confirm Delete", f"Delete coord ID {rid}?", QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes:
            return
        self.db.delete_coord(rid)
        self.coord_table.removeRow(row)
        self.status_label.setText(f"Status: Coord ID {rid} deleted.")

    def _delete_selected_region(self):
        row = self.region_table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Select Row", "Please select a region row to delete.")
            return
        rid = int(self.region_table.item(row, 0).text())
        if QMessageBox.question(self, "Confirm Delete", f"Delete region ID {rid}?", QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes:
            return
        self.db.delete_region(rid)
        self.region_table.removeRow(row)
        self.status_label.setText(f"Status: Region ID {rid} deleted.")

    # ---------------- Close ----------------
    def closeEvent(self, event):
        try:
            self.hk_thread.stop()
        except Exception:
            pass
        event.accept()

# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

    app = QApplication(sys.argv)
    w = MouseRegionApp()
    w.show()
    sys.exit(app.exec_())
