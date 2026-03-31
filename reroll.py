import pyautogui
from PIL import Image
import pytesseract
import time
import cv2
import numpy as np
import os
import variable
import requests
import sys
import json
import io
from dotenv import load_dotenv

verify_first_roll = True

class RerollEngine:
    def __init__(self, log_callback):
        """
        Khởi tạo Engine xử lý logic game.
        :param log_callback: Hàm để gửi tin nhắn (log) về giao diện UI.
        """
        load_dotenv()
        self.log = log_callback 
        self.is_running = False
        self.cfg = variable.Layout_241_with_bans # Mặc định ban đầu
        self.verify = variable.VERIFY
        
        # Cấu hình Tesseract
        pytesseract.pytesseract.tesseract_cmd = variable.TESSERACT_CMD
        
        # Ép chuẩn đầu ra UTF-8
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # --- CÁC HÀM TIỆN ÍCH HỖ TRỢ ---
    def click_location(self, location):
        if not self.is_running: return
        pyautogui.moveTo(location[0], location[1])
        pyautogui.click()

    def preprocess_image(self, image):
        image = cv2.resize(image, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        kernel = np.ones((1, 1), np.uint8)
        binary = cv2.dilate(binary, kernel, iterations=1)
        return cv2.erode(binary, kernel, iterations=1)

    def read_text(self, location):
        screenshot = pyautogui.screenshot(region=location)
        screenshot.save('screenshot_test.png')
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        preprocessed_image = self.preprocess_image(screenshot)
        return pytesseract.image_to_string(preprocessed_image, config='--psm 6').lower()

    def get_dominant_color_hex(self, path="screenshot_test.png", k=3):
        if not os.path.exists(path): return None
        img = cv2.imread(path)
        if img is None: return None
        pixels = img.reshape(-1, 3).astype(np.float32)
        kk = min(k, pixels.shape[0])
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, labels, centers = cv2.kmeans(pixels, kk, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
        dominant_bgr = centers[int(np.argmax(np.bincount(labels.flatten())))].astype(int)
        rgb = tuple(int(x) for x in dominant_bgr[::-1])
        return "#{:02x}{:02x}{:02x}".format(*rgb)

    def send_notification(self, title, content):
        device_key = os.getenv("BARK_KEY")
        if not device_key: return
        url = f"https://api.day.app/{device_key}/{title}/{content}"
        try: requests.get(url)
        except: pass

    # --- LOGIC XỬ LÝ CHÍNH ---
    def check_substat_logic(self, locked_subs):
        data = self.cfg.AFTER_ROLL_COORDS
        collected = 0
        verified = 0
        for i in list(locked_subs):
            if not self.is_running: break
            sub_key = f"SubLock{i}"
            text_content = self.read_text(data[sub_key]["CheckSubstat"])
            
            if "anc" not in text_content: continue
            
            self.read_text(data[sub_key]["LockIconImage"])
            current_color = self.get_dominant_color_hex()
            
            if current_color != '#494675':
                collected += 1
            elif current_color == '#494675' and "anc" in text_content:
                self.log(f"-> Locking Sub {i}...")
                collected += 1
                self.click_location(data[sub_key]["LockIcon"])
                locked_subs.remove(i)
            
        self.verify = True if verified > 0 else False
        time.sleep(1)
        self.click_location(data["exit_icon"])
        time.sleep(2)
        self.click_location(data["check_icon"])
        time.sleep(2)
        return collected

    def sub_locked_initial_check(self, locked_subs):
        data = self.cfg.AFTER_ROLL_COORDS
        collected = 0 
        for i in range(1, self.cfg.TARGET_SUBS + 1):
            if not self.is_running: break
            sub_key = f"SubLock{i}"
            self.read_text(data[sub_key]["LockIconImage"])
            if self.get_dominant_color_hex() != '#494675':
                if i in locked_subs:
                    locked_subs.remove(i)
                    self.log(f"Ignore sub {i} (Already locked)")
                    collected += 1
        return collected

    def reroll_action(self):
        self.click_location(self.cfg.MOD_OPTIONS)
        time.sleep(1)
        self.click_location(self.cfg.REROLL_EFFECTS)
        time.sleep(1)
        self.click_location(self.cfg.AUTO_REROLL_BUTTON)
        time.sleep(1)
        verify = self.read_text(variable.VERIFICATION_BUTTON_YES_REGION).lower() 
        if "yes" in verify:
            self.click_location(variable.VERIFICATION_BUTTON_YES)
        
        self.log(f"Rolling ({variable.ROLL_TIME}s)...")
        # Chia nhỏ thời gian chờ để có thể dừng bot ngay lập tức
        for _ in range(variable.ROLL_TIME):
            if not self.is_running: break
            time.sleep(1)

    def run_one_mod(self, mod_info):
        global verify_first_roll
        verify_first_roll = True
        """Hàm thực hiện roll trọn vẹn cho 1 Mod"""
        mod_name = mod_info["name"]
        layout_name = mod_info["layout"]        
        try:
            self.cfg = getattr(variable, layout_name)
            self.cfg.MOD_TO_ROLL_ICON = variable.MOD_LOCATION[mod_name]
        except Exception as e:
            self.log(f"Config error {mod_name}: {e}")
            return False 

        self.log(f"--- Starting: {mod_name} ({layout_name}) ---")
        locked_subs_copy = list(range(1, self.cfg.TARGET_SUBS + 1))
        collected_subs = 0
        sub_checked = False

        while self.is_running:
            self.click_location(self.cfg.MOD_TO_ROLL_ICON)
            time.sleep(1.5)
            if not verify_first_roll:
                self.click_location(self.cfg.MOD_OPTIONS_DEBUG)
                time.sleep(1) 

            if not sub_checked:
                self.click_location(self.cfg.MOD_OPTIONS)
                time.sleep(1)
                self.click_location(self.cfg.REROLL_EFFECTS)
                time.sleep(1)
                collected_subs = self.sub_locked_initial_check(locked_subs_copy)
                sub_checked = True
                verify_first_roll = False 
                self.click_location(self.cfg.AFTER_ROLL_COORDS["exit_icon"])

            self.reroll_action()
            if not self.is_running: break

            result = self.read_text(self.cfg.AUTO_REROLL_TEXT_REGION)
            if "reroll" in result:
                new_collected = self.check_substat_logic(locked_subs_copy)
                collected_subs += new_collected
                self.log(f"Progress: {collected_subs}/{self.cfg.TARGET_SUBS} lines of sub")
                
                if collected_subs >= self.cfg.TARGET_SUBS:
                    self.send_notification(f"Done {mod_name}", f"Collected {collected_subs} lines of substats.")
                    self.click_location((1115, 60))
                    time.sleep(1)  # Đợi load mod mới
                    return True # Hoàn thành mod này

            # Reset Tower
            self.log("Reset Tower...")
            self.click_location(self.cfg.EXIT_TOWER_BUTTON)
            time.sleep(4)
            self.click_location(self.cfg.TOWER_ICON)
            time.sleep(20) # Chờ load
            result_loading = self.read_text(self.cfg.LOADING_SCREEN_CHECK_REGION).lower()
            while "techtree" in result_loading:
                time.sleep(5)
                result_loading = self.read_text(self.cfg.LOADING_SCREEN_CHECK_REGION).lower()
                        
            self.click_location(self.cfg.MOD_ICON)
            time.sleep(1)
        
        return False