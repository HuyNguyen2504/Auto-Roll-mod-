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
import io
from dotenv import load_dotenv
load_dotenv()
cfg = variable.Layout_241_with_bans  # <--- IMPORT FILE SETTINGS 

# Ép hệ thống in ra chuẩn UTF-8 để không bị lỗi 'charmap'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Cấu hình Tesseract từ file settings
pytesseract.pytesseract.tesseract_cmd = variable.TESSERACT_CMD

def send_to_iphone(title, content):
    # Thay 'Your_Key' bằng mã số bạn thấy trong app Bark trên iPhone
    device_key = os.getenv("BARK_KEY")
    
    # Cấu trúc URL của Bark: https://api.day.app/{key}/{title}/{content}
    url = f"https://api.day.app/{device_key}/{title}/{content}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Notification sent successfully!")
        else:
            print("Error!")
    except Exception as e:
        print(f"Error 404: {e}")

def preprocess_image(image):
    # Resize the image for better accuracy
    image = cv2.resize(image, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    kernel = np.ones((1, 1), np.uint8)
    binary = cv2.dilate(binary, kernel, iterations=1)
    binary = cv2.erode(binary, kernel, iterations=1)
    
    return binary

def read_text(location):
    # Take a screenshot of the box specified
    screenshot = pyautogui.screenshot(region=location)
    screenshot.save('screenshot_test.png')
    
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    preprocessed_image = preprocess_image(screenshot)
    
    # Use pytesseract to read text
    text = pytesseract.image_to_string(preprocessed_image, config='--psm 6')
    return text

def click_location(location):
    pyautogui.moveTo(location[0], location[1])
    pyautogui.click()

def get_dominant_color_hex(path="screenshot_test.png", k=3):
    if not os.path.exists(path):
        return None

    img = cv2.imread(path)  # BGR
    if img is None:
        return None

    pixels = img.reshape(-1, 3).astype(np.float32)
    kk = min(k, pixels.shape[0])
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(pixels, kk, None, criteria, 10, cv2.KMEANS_PP_CENTERS)

    counts = np.bincount(labels.flatten())
    dom_idx = int(np.argmax(counts))
    dominant_bgr = centers[dom_idx].astype(int)

    rgb = tuple(int(x) for x in dominant_bgr[::-1])
    return "#{:02x}{:02x}{:02x}".format(*rgb)

verify = variable.VERIFY
Locked_subs = list(range(1, cfg.TARGET_SUBS + 1))
def check_substat():
    # Hàm này giờ tự lấy dữ liệu từ cfg.AFTER_ROLL_COORDS
    data = cfg.AFTER_ROLL_COORDS
    collected = 0
    verified = 0
    global Locked_subs
    for i in range(1, cfg.TARGET_SUBS + 1):  
        if i not in Locked_subs:
            continue
        sub_key = f"SubLock{i}"
        # Đọc text
        text_content = str(read_text(data[sub_key]["CheckSubstat"])).lower()        
        if ("anc" not in text_content):
            continue
        # Đọc màu
        read_text(data[sub_key]["LockIconImage"])
        current_color = get_dominant_color_hex()
        # print(f"Checking {sub_key}: {current_color}")
        
        print(f"sub{i}: {current_color}, {text_content}")
        if current_color != '#494675':
            collected += 1
        elif current_color == '#494675' and "anc" in text_content:
            #  print(f"--> Locking {sub_key}")
             collected += 1
             click_location(data[sub_key]["LockIcon"])
             Locked_subs.remove(i)
        if "myth" in text_content:
            verified += 1
    global verify
    if verified > 0:
        verify = True
    else:
        verify = False             
    time.sleep(1)
    click_location(data["exit_icon"])
    time.sleep(1)
    click_location(data["check_icon"])
    time.sleep(2)
    return collected
 
def reroll_after_saved():
    """
    Hàm này thực hiện thao tác click reroll.
    Không cần truyền tham số vì lấy trực tiếp từ file settings (cfg).
    """
    # click mod options
    click_location(cfg.MOD_OPTIONS)
    time.sleep(0.5)

    # click reroll effects
    click_location(cfg.REROLL_EFFECTS)
    time.sleep(0.5)
    
    # Start autoroll
    click_location(cfg.AUTO_REROLL_BUTTON)
    
    if verify:
        time.sleep(1)
        click_location(cfg.VERIFICATION_BUTTON_YES)
        
    time.sleep(variable.ROLL_TIME)    

def Sub_locked():
    data = cfg.AFTER_ROLL_COORDS
    global Locked_subs
    collected = 0 
    for i in range(1, cfg.TARGET_SUBS + 1):  
        sub_key = f"SubLock{i}"
        # Đọc text
        text_content = str(read_text(data[sub_key]["CheckSubstat"])).lower()        
        if ("anc" not in text_content) or ("anc" in text_content and i not in Locked_subs):
            continue
        # Đọc màu
        read_text(data[sub_key]["LockIconImage"])
        current_color = get_dominant_color_hex()
        # print(f"Checking {sub_key}: {current_color}")
        if current_color != '#494675' and "anc" in text_content:
             Locked_subs.remove(i)   
             collected += 1
    return collected

Sub_checked = False
# --- MAIN EXECUTION ---
def start_bot():
    time.sleep(1)
    check = True
    collected = 0
    while check:
        # print("Starting main loop.")
        
        # 1. Open the tower
        click_location(cfg.TOWER_ICON)
        time.sleep(20)
        
        # 2. Check loading screen
        result = read_text(cfg.LOADING_SCREEN_CHECK_REGION).lower()
        while "techtree" in result:
            time.sleep(5)
            result = read_text(cfg.LOADING_SCREEN_CHECK_REGION).lower()
            # print(f"Loading status: {result}") 
        time.sleep(3)    
        # 3. Open mods & select cannon
        click_location(cfg.MOD_ICON)
        time.sleep(1)
        click_location(cfg.MOD_TO_ROLL_ICON)
        time.sleep(1)
        global Sub_checked
        # 4. Open mod options (Double click fix)
        click_location(cfg.MOD_OPTIONS_DEBUG)
        if(Sub_checked == False):
            click_location(cfg.MOD_OPTIONS_DEBUG)
            click_location(cfg.REROLL_EFFECTS)
            collected = Sub_locked()
            Sub_checked = True
            click_location(cfg.AFTER_ROLL_COORDS["exit_icon"])
        # Gọi hàm reroll lần đầu
        reroll_after_saved()

        # 5. Loop Reroll logic
        result = read_text(cfg.AUTO_REROLL_TEXT_REGION).lower()
        # print(f"Reroll text detected: {result}")
        
        while "reroll" in result:
            collected_subs = check_substat() + collected 
            # print(f"Subs collected: {collected_subs}/{variable.TARGET_SUBS}")
            if collected_subs >= cfg.TARGET_SUBS:
                send_to_iphone("Reroll Completed", f"Collected {collected_subs} subs, stopping script.")
                check = False
                break            
            reroll_after_saved() # Gọi hàm không cần tham số
            result = read_text(cfg.AUTO_REROLL_TEXT_REGION).lower()
        if not check:
            continue    
        # 6. Exit condition
        click_location(cfg.EXIT_TOWER_BUTTON)
        # print("Finished loop, exiting and repeating.")
        time.sleep(4)

if __name__ == "__main__":
    start_bot()