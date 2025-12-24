import pyautogui
import cv2
import numpy as np
import pytesseract
import time
import pydirectinput
import os
import requests
import sys
import io
from dotenv import load_dotenv

def send_to_iphone(title, content):
    # Thay 'Your_Key' bằng mã số bạn thấy trong app Bark trên iPhone
    device_key = os.getenv("BARK_DEVICE_KEY") 
    
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

# --- IMPORT FILE VARIABLE ---
import variable
from reroll import cfg as reroll_cfg

# CHỌN LAYOUT (PROFILE) BẠN MUỐN TEST Ở ĐÂY
cfg = reroll_cfg
# cfg = variable.Layout_241  # <--- IMPORT FILE SETTINGS

pytesseract.pytesseract.tesseract_cmd = variable.TESSERACT_CMD # Lấy đường dẫn từ file variable luôn

def preprocess_image(image):
    # Resize the image for better accuracy (e.g., scaling by 1.5x)
    image = cv2.resize(image, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian Blurring to reduce noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply thresholding (convert image to black and white)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Optionally apply dilation and erosion to further clean up the image
    kernel = np.ones((1, 1), np.uint8)
    binary = cv2.dilate(binary, kernel, iterations=1)
    binary = cv2.erode(binary, kernel, iterations=1)
    
    return binary

def read_text(location):
    # Ensure screenshots directory exists
    os.makedirs("screenshots", exist_ok=True)

    # Take a screenshot of the box specified, and read the text
    screenshot = pyautogui.screenshot(region=location)
    screenshot.save("screenshots\\screenshot_test.png")

    # Convert the screenshot to a format suitable for OpenCV
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    # Preprocess the image for better OCR accuracy
    preprocessed_image = preprocess_image(screenshot)

    # Save the preprocessed image for debugging
    cv2.imwrite("screenshots\\preprocessed_screenshot_test.png", preprocessed_image)

    # Use pytesseract to read text from the preprocessed image
    text = pytesseract.image_to_string(preprocessed_image, config="--psm 6")

    return text

def calibrate_pointer(location):
    print(f"Moving to: {location}")
    time.sleep(1)
    pydirectinput.moveTo(*location)

def click_on(location):
    pydirectinput.moveTo(*location)
    pydirectinput.click()

def calibrate_text_box(location, box):
    time.sleep(1)
    pydirectinput.moveTo(*location)
    # Đọc text từ vùng box được truyền vào
    print(f"Reading text at region: {box}")
    print(f"Result: {read_text(box)}")

def get_dominant_color_hex(path="screenshots\\screenshot_test.png", k=3):
    """
    Trả về màu dominant duy nhất dưới dạng hex string (e.g. '#aabbcc').
    Trả về None nếu file không tồn tại hoặc không thể đọc.
    """
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

    # convert BGR -> RGB -> hex
    rgb = tuple(int(x) for x in dominant_bgr[::-1])
    return "#{:02x}{:02x}{:02x}".format(*rgb)

# ==========================================
# CÁC HÀM TEST (ĐÃ CẬP NHẬT DÙNG BIẾN CFG)
# ==========================================
collected_subs = 0
def check_location():
    # print(f"Checking location using profile: {cfg.__name__}")
    # Test đọc thử ảnh ổ khóa của Sub 1
    # read_text(cfg.AFTER_ROLL_COORDS["SubLock1"]["LockIconImage"])
    # Test pointer location
    calibrate_pointer(cfg.MOD_OPTIONS)
    calibrate_pointer(cfg.MOD_OPTIONS_DEBUG)
    
    # Test text from image
    # calibrate_text_box((745, 375), cfg.AFTER_ROLL_COORDS["SubLock6"]["LockIconImage"])
    
    # print(f"Color: {get_dominant_color_hex()}")

    # check all sub
    collected = 0
    for i in range(1, len(cfg.AFTER_ROLL_COORDS) - 1):  # Trừ 2 vì có 2 key không phải SubLock
        sub_key = f"SubLock{i}"
        sub_data = cfg.AFTER_ROLL_COORDS[sub_key] # Lấy dict con từ file variable
        
        # Chụp ảnh vùng icon khóa để lấy màu
        read_text(sub_data["LockIconImage"])
        color = get_dominant_color_hex()
        calibrate_pointer(sub_data["LockIcon"])
        # Đọc text substat
        text_content = str(read_text(sub_data["CheckSubstat"])).lower()
        
        print(f"{sub_key}: {color}, {text_content}")
        if color != '#494675':
            collected += 1
        if color == '#494675' and "ances" in text_content:          
            print(f"--> Would click lock at: {sub_data['LockIcon']}")
            click_on(sub_data["LockIcon"])
    if collected <= 5:
        collected = 0
    else:
        global collected_subs
        # print(f"Total collected subs: {collected}")
        collected_subs = collected
        # print(f"Total collected subs (global): {collected_subs}")

def click_test():
    print("Running click test...")
    # Các biến này lấy từ file variable.py thông qua cfg
    click_on(cfg.MOD_TO_ROLL_ICON)
    time.sleep(1)
    
    click_on(cfg.MOD_OPTIONS_DEBUG)
    # click_on(cfg.MOD_OPTIONS) # Có thể bỏ comment nếu cần test cả 2
    time.sleep(1)
    
    click_on(cfg.REROLL_EFFECTS)
    time.sleep(1)
    
    calibrate_pointer(cfg.AUTO_REROLL_BUTTON)

# --- KHU VỰC CHẠY LỆNH ---

# remove comment in test line:
print(read_text(cfg.AUTO_REROLL_TEXT_REGION))
check_location()
if collected_subs >= 6:
    send_to_iphone("Reroll Test", f"Collected {collected_subs} subs during test.")
# print(len(cfg.AFTER_ROLL_COORDS))
# print(collected_subs)
# time.sleep(1)
# sub_key = f"SubLock{7}"
# sub_data = cfg.AFTER_ROLL_COORDS[sub_key] # Lấy dict con từ file variable

# print(read_text(sub_data["CheckSubstat"]))
# print(get_dominant_color_hex())
# click_test()

# Test lẻ một giá trị:
# read_text(cfg.AFTER_ROLL_COORDS["SubLock1"]["LockIconImage"])
# print(get_dominant_color_hex())