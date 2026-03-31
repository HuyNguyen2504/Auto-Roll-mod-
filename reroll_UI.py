import customtkinter as ctk
from tkinter import messagebox
from threading import Thread
import json
import time
import os
import re
import variable
from reroll import RerollEngine 

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AutoRerollMicroUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # --- CẤU HÌNH VỊ TRÍ & KÍCH THƯỚC ---
        width, height = 490, 450 
        x, y = 1290, 10 # Xuất hiện ở góc trên bên trái
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.title("Auto Reroll Bot")
        self.attributes("-topmost", True)

        self.engine = RerollEngine(log_callback=self.status_print)

        # --- GIAO DIỆN ---
        self.grid_columnconfigure((0, 1), weight=1)
        
        # 1. Header
        self.header = ctk.CTkLabel(self, text='AUTO REROLL BOT', font=("Roboto", 16, "bold"))
        self.header.grid(row=0, column=0, columnspan=2, pady=5)

        # 2. Dropdowns chọn Mod/Layout
        small_font = ("Roboto", 11)
        self.mod_select = ctk.CTkOptionMenu(self, values=list(variable.MOD_LOCATION.keys()), width=160, font=small_font)
        self.mod_select.grid(row=1, column=0, padx=5, pady=2)
        self.mod_select.set("Mod")

        layouts = [n for n in dir(variable) if n.startswith("Layout_")]
        self.layout_select = ctk.CTkOptionMenu(self, values=layouts, width=160, font=small_font)
        self.layout_select.grid(row=1, column=1, padx=5, pady=2)
        self.layout_select.set("Layout")

        # 3. Roll Time
        self.time_entry = ctk.CTkEntry(self, placeholder_text="Time (s)", width=80)
        self.time_entry.insert(0, str(variable.ROLL_TIME))
        self.time_entry.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.time_btn = ctk.CTkButton(self, text="Set Time (s)", width=100, command=self.update_roll_time)
        self.time_btn.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # 4. TÍNH NĂNG MỚI: QUẢN LÝ XÓA TỰ DO
        delete_frame = ctk.CTkFrame(self, fg_color="transparent")
        delete_frame.grid(row=3, column=0, columnspan=2, pady=5)

        self.delete_idx_entry = ctk.CTkEntry(delete_frame, placeholder_text="Enter ID", width=60)
        self.delete_idx_entry.pack(side="left", padx=5)

        self.delete_btn = ctk.CTkButton(delete_frame, text="Delete ID", width=90, fg_color="#A12F2F", hover_color="#7A2424", command=self.delete_mod_by_index)
        self.delete_btn.pack(side="left", padx=5)

        self.clear_all_btn = ctk.CTkButton(delete_frame, text="Clear All", width=80, fg_color="#3d3d3d", command=self.clear_all_queue)
        self.clear_all_btn.pack(side="left", padx=5)

        # 5. Buttons chính
        self.add_btn = ctk.CTkButton(self, text="ADD MOD", width=150, height=30, command=self.add_to_json)
        self.add_btn.grid(row=4, column=0, padx=5, pady=10)

        self.start_btn = ctk.CTkButton(self, text="START BOT (5s delay)", width=150, height=30, fg_color="green", command=self.toggle_bot)
        self.start_btn.grid(row=4, column=1, padx=5, pady=10)

        # 6. Bảng hiển thị
        self.queue_table = ctk.CTkTextbox(self, height=200, font=("Consolas", 10))
        self.queue_table.grid(row=5, column=0, padx=(10, 2), pady=(0, 10), sticky="nsew")

        self.status_table = ctk.CTkTextbox(self, height=200, font=("Consolas", 10))
        self.status_table.grid(row=5, column=1, padx=(2, 10), pady=(0, 10), sticky="nsew")
        
        self.update_queue_display()

    # --- LOGIC XÓA TỰ DO ---
    def delete_mod_by_index(self):
        """Xóa một mod cụ thể dựa trên số ID hiển thị trong bảng"""
        idx_str = self.delete_idx_entry.get()
        if not idx_str.isdigit():
            messagebox.showwarning("Warning", "Please enter the ID (index) of the mod you want to delete!")
            return
        
        target_idx = int(idx_str) - 1 # Chuyển sang index của mảng (bắt đầu từ 0)
        
        try:
            with open('mods_config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            if 0 <= target_idx < len(config["data"]):
                removed = config["data"].pop(target_idx)
                with open('mods_config.json', 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=4, ensure_ascii=False)
                
                self.status_print(f"System: Deleted {idx_str} ({removed['name']})")
                self.delete_idx_entry.delete(0, 'end')
                self.update_queue_display()
            else:
                messagebox.showerror("Error", f"No mod found with ID {idx_str}!")
        except Exception as e:
            self.status_print(f"Error occurred while deleting: {e}")

    def clear_all_queue(self):
        """Xóa toàn bộ hàng đợi"""
        if messagebox.askyesno("Confirm", "Do you want to clear the entire queue?"):
            try:
                with open('mods_config.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
                config["data"] = []
                with open('mods_config.json', 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=4, ensure_ascii=False)
                self.update_queue_display()
                self.status_print("System: Cleared the entire queue.")
            except Exception as e:
                self.status_print(f"Error: {e}")

    # --- CÁC HÀM HỖ TRỢ KHÁC ---
    def update_roll_time(self):
        new_time = self.time_entry.get()
        if not new_time.isdigit():
            messagebox.showerror("Error", "Please enter an integer for Roll Time!")
            return
        try:
            with open('variable.py', 'r', encoding='utf-8') as f:
                content = f.read()
            new_content = re.sub(r'ROLL_TIME\s*=\s*\d+', f'ROLL_TIME = {new_time}', content)
            with open('variable.py', 'w', encoding='utf-8') as f:
                f.write(new_content)
            variable.ROLL_TIME = int(new_time)
            messagebox.showinfo("Success", f"Roll Time saved = {new_time}s")
        except Exception as e:
            messagebox.showerror("Error", f"Cannot write to file: {e}")

    def status_print(self, message):
        ts = time.strftime("%H:%M:%S")
        self.status_table.insert("end", f"[{ts}] {message}\n")
        self.status_table.see("end")

    def add_to_json(self):
        mod = self.mod_select.get()
        layout = self.layout_select.get()
        if mod == "Mod" or layout == "Layout":
            messagebox.showwarning("Warning", "Please select both Mod and Layout!")
            return
        try:
            with open('mods_config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            config["data"].append({"name": mod, "layout": layout})
            with open('mods_config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            self.update_queue_display()
        except Exception as e:
            self.status_print(f"Lỗi thêm mod: {e}")

    def update_queue_display(self):
        """Hiển thị hàng đợi kèm theo cột ID để người dùng biết số cần xóa"""
        self.queue_table.delete("1.0", "end")
        self.queue_table.insert("end", f"{'ID':<4}| {'MOD NAME':<15}\n" + "-"*22 + "\n")
        try:
            with open('mods_config.json', 'r', encoding='utf-8') as f:
                data = json.load(f).get("data", [])
                for i, item in enumerate(data, 1):
                    self.queue_table.insert("end", f"{i:<4}| {item['name']}\n")
        except: pass

    def toggle_bot(self):
        if not self.engine.is_running:
            import reroll_test
            reroll_test.verify_first_roll = True
            self.engine.is_running = True
            self.start_btn.configure(text="STOP BOT", fg_color="red")
            Thread(target=self.main_bot_loop, daemon=True).start()
        else:
            self.engine.is_running = False
            self.start_btn.configure(text="START BOT (5s delay)", fg_color="green")

    def main_bot_loop(self):
        time.sleep(5) # Delay 5s trước khi bắt đầu
        while self.engine.is_running:
            try:
                with open('mods_config.json', 'r', encoding='utf-8') as f:
                    queue = json.load(f).get("data", [])
            except: queue = []
            
            if not queue:
                self.status_print("Out of mods to roll. Stopping bot.")
                self.engine.is_running = False
                self.after(0, lambda: self.start_btn.configure(text="START BOT", fg_color="green"))
                break

            current_mod = queue[0]
            self.after(0, self.update_queue_display)
            success = self.engine.run_one_mod(current_mod)

            if success and self.engine.is_running:
                # Xóa mod vừa làm xong (luôn là vị trí số 0)
                self.remove_first_mod_from_json()
                self.after(0, self.update_queue_display) 
                # if len(queue) > 1:  # Kiểm tra nếu còn mod nào trong hàng đợi
                #     self.click_location(variable.MOD_LOCATION[queue[0]["name"]])
                #     time.sleep(3)

    def remove_first_mod_from_json(self):
        try:
            with open('mods_config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            if config["data"]:
                removed = config["data"].pop(0)
                with open('mods_config.json', 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=4, ensure_ascii=False)
                self.status_print(f"Completed: {removed['name']}")
        except: pass

if __name__ == "__main__":
    app = AutoRerollMicroUI()
    app.mainloop()