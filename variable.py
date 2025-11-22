# variable.py

# --- MAIN SETTING ---
TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe' #Change this to your Tesseract installation path
VERIFY = False       
ROLL_TIME = 20       
TARGET_SUBS = 6      
START_SUBS_COUNT = 4 

# --- PROFILE 241 (CẤU HÌNH HIỆN TẠI CỦA BẠN) ---
class Layout_241:
    # Coordinates
    TOWER_ICON = (780, 340)
    MOD_ICON = (1000, 980)
    MOD_TO_ROLL_ICON = (850, 700)
    CANNON_ICON = (850, 250)
    ARMOR_ICON = (850, 350)
    CORE_ICON = (1400, 400)
    GENERATOR_ICON = (1400, 250)

    MOD_OPTIONS = (1115, 330)
    MOD_OPTIONS_DEBUG = (1115, 320)
    REROLL_EFFECTS = (1100, 360)
    AUTO_REROLL_BUTTON = (850, 710)
    VERIFICATION_BUTTON_YES = (1070, 670)
    EXIT_TOWER_BUTTON = (775, 14)
    MENU_BUTTON = (1790, 225)
    EMPTY_SPACE = (1400, 300)

    # Regions
    AUTO_REROLL_TEXT_REGION = (845, 705, 120, 35)
    LOADING_SCREEN_CHECK_REGION = (870, 680, 150, 70)

    # Substats Dictionary
    AFTER_ROLL_COORDS = {
        "exit_icon": (1135, 350),
        "check_icon": (1070, 950),
        "SubLock1": {"CheckSubstat": (774, 390, 170, 30), "LockIcon": (1135, 390), "LockIconImage": (1130, 385, 15, 15)},
        "SubLock2": {"CheckSubstat": (774, 430, 170, 30), "LockIcon": (1135, 430), "LockIconImage": (1130, 425, 15, 15)},
        "SubLock3": {"CheckSubstat": (774, 465, 170, 30), "LockIcon": (1135, 470), "LockIconImage": (1130, 465, 15, 15)},
        "SubLock4": {"CheckSubstat": (774, 505, 170, 30), "LockIcon": (1135, 510), "LockIconImage": (1130, 505, 15, 15)},
        "SubLock5": {"CheckSubstat": (774, 545, 100, 30), "LockIcon": (1135, 550), "LockIconImage": (1130, 545, 15, 15)},
        "SubLock6": {"CheckSubstat": (774, 575, 70, 30),  "LockIcon": (1135, 590), "LockIconImage": (1130, 585, 15, 15)}
    }

# --- PROFILE 161 (BẠN CẦN ĐIỀN TỌA ĐỘ MỚI VÀO ĐÂY) ---
class Layout_161:
    # Coordinates
    TOWER_ICON = (780, 340)
    MOD_ICON = (1000, 980)
    MOD_TO_ROLL_ICON = (1163, 601)
    CANNON_ICON = (850, 250)
    ARMOR_ICON = (850, 350)
    CORE_ICON = (1400, 400)
    GENERATOR_ICON = (1400, 250)

    MOD_OPTIONS = (1102, 365)
    MOD_OPTIONS_DEBUG = (1102, 365)
    REROLL_EFFECTS = (1088, 402)
    AUTO_REROLL_BUTTON = (927, 682)
    VERIFICATION_BUTTON_YES = (1070, 670)
    EXIT_TOWER_BUTTON = (775, 14)
    MENU_BUTTON = (1790, 225)
    EMPTY_SPACE = (1400, 300)

    # Regions
    AUTO_REROLL_TEXT_REGION = (843, 668, 130, 23)
    LOADING_SCREEN_CHECK_REGION = (870, 680, 150, 70)

    # Substats Dictionary
    AFTER_ROLL_COORDS = {
        "exit_icon": (1143, 397),
        "check_icon": (1078, 865),
        "SubLock1": {"CheckSubstat": (774, 427, 72, 20), "LockIcon": (1135, 431), "LockIconImage": (1129, 427, 15, 15)},
        "SubLock2": {"CheckSubstat": (774, 465, 73, 20), "LockIcon": (1135, 469), "LockIconImage": (1129, 465, 15, 15)},
        "SubLock3": {"CheckSubstat": (774, 504, 71, 20), "LockIcon": (1135, 511), "LockIconImage": (1129, 503, 15, 15)},
        "SubLock4": {"CheckSubstat": (774, 542, 74, 20), "LockIcon": (1135, 553), "LockIconImage": (1129, 541, 15, 15)},
        "SubLock5": {"CheckSubstat": (774, 579, 72, 20), "LockIcon": (1135, 584), "LockIconImage": (1129, 579, 15, 15)},
        "SubLock6": {"CheckSubstat": (774, 617, 70, 20),  "LockIcon": (1135, 626), "LockIconImage": (1129, 615, 15, 15)}
    }

# --- PROFILE 201 (BẠN CẦN ĐIỀN TỌA ĐỘ MỚI VÀO ĐÂY) ---
class Layout_201:
    # Coordinates
    TOWER_ICON = (780, 340)
    MOD_ICON = (1000, 980)
    MOD_TO_ROLL_ICON = (1051, 598)
    CANNON_ICON = (850, 250)
    ARMOR_ICON = (850, 350)
    CORE_ICON = (1400, 400)
    GENERATOR_ICON = (1400, 250)

    MOD_OPTIONS = (1087, 345)
    MOD_OPTIONS_DEBUG = (1089, 345)
    REROLL_EFFECTS = (1073, 388)
    AUTO_REROLL_BUTTON = (905, 704)
    VERIFICATION_BUTTON_YES = (1070, 670)
    EXIT_TOWER_BUTTON = (775, 14)
    MENU_BUTTON = (1790, 225)
    EMPTY_SPACE = (1400, 300)

    # Regions
    AUTO_REROLL_TEXT_REGION = (828, 683, 162, 37)
    LOADING_SCREEN_CHECK_REGION = (870, 680, 150, 70)

    # Substats Dictionary
    AFTER_ROLL_COORDS = {
        "exit_icon": (1138, 377),
        "check_icon": (1032, 901),
        "SubLock1": {"CheckSubstat": (774, 406, 72, 20), "LockIcon": (1135, 419), "LockIconImage": (1129, 406, 15, 15)},
        "SubLock2": {"CheckSubstat": (774, 448, 73, 20), "LockIcon": (1135, 459), "LockIconImage": (1129, 447, 15, 15)},
        "SubLock3": {"CheckSubstat": (774, 483, 71, 20), "LockIcon": (1135, 494), "LockIconImage": (1129, 483, 15, 15)},
        "SubLock4": {"CheckSubstat": (774, 523, 74, 20), "LockIcon": (1135, 534), "LockIconImage": (1129, 520, 15, 15)},
        "SubLock5": {"CheckSubstat": (776, 559, 72, 20), "LockIcon": (1135, 569), "LockIconImage": (1129, 559, 15, 15)},
        "SubLock6": {"CheckSubstat": (774, 598, 70, 20),  "LockIcon": (1135, 606), "LockIconImage": (1129, 598, 15, 15)}
    }