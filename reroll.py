import pyautogui
from PIL import Image
import pytesseract
import time
import cv2
import numpy as np
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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
    # Take a screenshot of the box specified, and read the text
    screenshot = pyautogui.screenshot(region=location)
    screenshot.save('screenshot_test.png')
    
    # Convert the screenshot to a format suitable for OpenCV
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    # Preprocess the image for better OCR accuracy
    preprocessed_image = preprocess_image(screenshot)
    
    # Save the preprocessed image for debugging
    cv2.imwrite('preprocessed_screenshot_test.png', preprocessed_image)
    
    # Use pytesseract to read text from the preprocessed image
    text = pytesseract.image_to_string(preprocessed_image, config='--psm 6')
    
    return text

# Function to click at a specified location
def click_location(location):
    pyautogui.moveTo(location[0], location[1])
    pyautogui.click()

def click_location2(location):
    pyautogui.moveTo(location[0], location[1])
    pyautogui.click()

def get_dominant_color_hex(path="screenshot_test.png", k=3):
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

def check_substat(After_roll):
    for i in range(1,7):
        read_text(After_roll[f"SubLock{i}"]["LockIconImage"])
        print(get_dominant_color_hex())
        if get_dominant_color_hex() == '#494675' and "ances" in str(read_text(After_roll[f"SubLock{i}"]["CheckSubstat"])).lower():           
            click_location(After_roll[f"SubLock{i}"]["LockIcon"])
    time.sleep(1)
    click_location(After_roll["exit_icon"])
    time.sleep(1)
    click_location(After_roll["check_icon"])
    time.sleep(1)

def reroll_after_saved(mod_options, reroll_effects, auto_reroll_button, verification_button_yes, roll_time, verify):
    # click mod options
    click_location(mod_options)
    time.sleep(0.5)

    # click reroll effects
    click_location(reroll_effects)
    time.sleep(0.5)
    # Start autoroll
    click_location(auto_reroll_button)
    
    if verify:
        time.sleep(1)
        click_location(verification_button_yes)
    time.sleep(roll_time)    
# click coords
tower_icon = (780, 340)
mod_icon = (1000, 980)
mod_to_roll_icon = (850, 700)
cannon_icon = (850, 250)
armor_icon = (850, 350)
core_icon = (1400, 400)
generator_icon = (1400, 250)
mod_options= (1115, 330)
mod_options_debug= (1115, 320)
reroll_effects = (1100, 360)
verification_button_yes = (1070, 670)
exit_tower_button = (775, 14)
menu_button = (1790, 225)
empty_space = (1400, 300)

auto_reroll_button = (850, 710)
auto_reroll_text = (845, 705, 120, 35)
auto_reroll_text_161 = (835, 700, 150, 27)
loading_screen_check = (870, 680, 150, 70)
After_roll = {
    "exit_icon": (1135, 350),
    "check_icon": (1070, 950),
    "SubLock1": {
        "CheckSubstat": (774, 390, 170, 30),
        "LockIcon": (1135, 390),
        "LockIconImage": (1130, 385, 15, 15)
    },
    "SubLock2": {
        "CheckSubstat": (774, 430, 170, 30),
        "LockIcon": (1135, 430),
        "LockIconImage": (1130, 425, 15, 15)
    },
    "SubLock3": {
        "CheckSubstat": (774, 465, 170, 30),
        "LockIcon": (1135, 470),
        "LockIconImage": (1130, 465, 15, 15)
    },
    "SubLock4": {
        "CheckSubstat": (774, 505, 170, 30),
        "LockIcon": (1135, 510),
        "LockIconImage": (1130, 505, 15, 15)
    },
    "SubLock5": {
        "CheckSubstat": (774, 545, 100, 30),
        "LockIcon": (1135, 550),
        "LockIconImage": (1130, 545, 15, 15)
    },
    "SubLock6": {
        "CheckSubstat": (774, 575, 70, 30),
        "LockIcon": (1135, 590),
        "LockIconImage": (1130, 585, 15, 15)
    }
}
# Verify box - if you are rolling a slot with myth/anc in it
verify = False

# Length of rolling window, longer = more shards spent but faster to get desired sub
roll_time = 20

end_script = False
cloud_save_counter = 0

time.sleep(1)

collected_subs = 4
number_of_subs_to_collect = 6

while True:
    print("Starting main loop.")
    # open the tower
    click_location(tower_icon)
    time.sleep(10)
    result = read_text(loading_screen_check).lower()
    while("techtree" in result):
        time.sleep(5)
        result = read_text(loading_screen_check).lower()
        print(result) 
    # open mods
    click_location2(mod_icon)
    time.sleep(1)

    # click desired mod icon
    click_location(cannon_icon)
    time.sleep(1)

    # click mod options - for some reason a single click fails, gotta use two clicks to open options
    click_location(mod_options_debug)
    reroll_after_saved()

    result = read_text(auto_reroll_text).lower()
    print(result)
    while "reroll" in result:
        check_substat(After_roll)
        collected_subs += 1
        reroll_after_saved(mod_options, reroll_effects, auto_reroll_button, verification_button_yes, roll_time, verify)
        result = read_text(auto_reroll_text).lower()
    # exit tower
    if collected_subs >= number_of_subs_to_collect:
        break
    click_location2(exit_tower_button)
    print("Finished loop, exiting and repeating.")
    time.sleep(3)
# check_substat(After_roll)
# read_text(After_roll["SubLock1"]["LockIconImage"])
# print(get_dominant_color_hex())