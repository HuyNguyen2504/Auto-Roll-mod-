import pyautogui
import cv2
import numpy as np
import pytesseract
import time
import pydirectinput
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
    time.sleep(1)
    pydirectinput.moveTo(*location)

def click_on(location):
    pydirectinput.moveTo(*location)
    pydirectinput.click()

def calibrate_text_box(location, box):
    time.sleep(1)
    pydirectinput.moveTo(*location)
    print(read_text(box))

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

# Remove comment (#) on which function you want to use, enter the coords you want to test, then run
# for pointer it will move mouse to the spot you selected in 2s. Check where it is, adjust, repeat
# for text box it will try read the text and print the result. It will be failing at first so check the saved
# screenshot to see what you captured, change the coords accordingly, repeat, until it reads the text correctly
# the four value field is (starting x coord, starting y coord, width from starting x, height(down) from starting y)

tower_icon = (780, 340)
mod_icon = (1000, 980)
mod_to_roll_icon = (850, 700)
cannon_icon = (850, 250)
armor_icon = (580, 350)
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

# (750, 375), (750, 375, 400, 35)
# (750, 415), (750, 415, 400, 35)


def check_location():
    # calibrate_pointer(cannon_icon)
    read_text(After_roll["SubLock1"]["LockIconImage"])
    # calibrate_pointer(mod_options)
    # calibrate_pointer(mod_options_debug)
    # calibrate_text_box((745, 375), After_roll["SubLock6"]["LockIconImage"])
    # print(get_dominant_color_hex())
    # for i in range(1, 7):
    #     read_text(After_roll[f"SubLock{i}"]["LockIconImage"])
    #     # print(get_dominant_color_hex())
    #     if get_dominant_color_hex() == '#494675' and "ances" in str(read_text(After_roll[f"SubLock{i}"]["CheckSubstat"])).lower():           
    #         click_on(After_roll[f"SubLock{i}"]["LockIcon"])
    # time.sleep(1)
    # click_on(After_roll["exit_icon"])
    # time.sleep(1)
    # click_on(After_roll["check_icon"])
    # time.sleep(1)

def click_test():
    click_on(mod_to_roll_icon)
    time.sleep(1)
    click_on(mod_options_debug)
    click_on(mod_options)
    time.sleep(1)
    click_on(reroll_effects)
    time.sleep(1)
    calibrate_pointer(auto_reroll_button)

check_location()
# click_test()
# read_text(After_roll["SubLock1"]["LockIconImage"])
# print(get_dominant_color_hex())