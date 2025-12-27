import os
from dotenv import load_dotenv
# --- MAIN SETTING ---
load_dotenv()
TESSERACT_CMD = os.getenv("TESSERACT_PATH") #Change this to your Tesseract installation path
VERIFY = False       
ROLL_TIME = 30        
MOD_LOCATION = {
    "Mod_1_1": (753, 586),
    "Mod_1_2": (872, 589),
    "Mod_1_3": (963, 602),
    "Mod_1_4": (1053, 592),
    "Mod_1_5": (1166, 595),
    "Mod_2_1": (742, 695),
    "Mod_2_2": (858, 699),
    "Mod_2_3": (961, 694),
    "Mod_2_4": (1056, 694),
    "Mod_2_5": (1157, 696),
    "Mod_3_1": (762, 792),
    "Mod_3_2": (862, 802),
    "Mod_3_3": (970, 796),
    "Mod_3_4": (1064, 796),
    "Mod_3_5": (1162, 796),
    "Cannon_main": (837, 260),
    "Cannon_ass": (745, 260),
    "Armor_main": (837, 360),
    "Armor_ass": (732, 376),
    "Generator_main": (1070, 260),
    "Generator_ass": (1182, 250),
    "Core_main": (1085, 384),
    "Core_ass": (1183, 374)
}

# --- PROFILE 241 (CẤU HÌNH HIỆN TẠI CỦA BẠN) ---
class Layout_241:
    # Coordinates
    TARGET_SUBS = 7
    TOWER_ICON = (780, 340)
    MOD_ICON = (1000, 980)
    MOD_TO_ROLL_ICON = MOD_LOCATION["Cannon_ass"]

    MOD_OPTIONS = (1115, 330)
    MOD_OPTIONS_DEBUG = (1115, 320)
    REROLL_EFFECTS = (1100, 360)
    AUTO_REROLL_BUTTON = (904, 748)
    VERIFICATION_BUTTON_YES = (1070, 670)
    EXIT_TOWER_BUTTON = (775, 14)
    MENU_BUTTON = (1790, 225)
    EMPTY_SPACE = (1400, 300)

    # Regions
    AUTO_REROLL_TEXT_REGION = (833, 735, 147, 25)
    LOADING_SCREEN_CHECK_REGION = (870, 680, 150, 70)

    # Substats Dictionary
    AFTER_ROLL_COORDS = {
        "exit_icon": (1143, 383),
        "check_icon": (1056, 943),
        "SubLock1": {"CheckSubstat": (774, 418, 61, 13), "LockIcon": (1135, 426), "LockIconImage": (1130, 418, 15, 15)},
        "SubLock2": {"CheckSubstat": (774, 456, 61, 13), "LockIcon": (1135, 465), "LockIconImage": (1130, 456, 15, 15)},
        "SubLock3": {"CheckSubstat": (774, 493, 61, 13), "LockIcon": (1135, 503), "LockIconImage": (1130, 494, 15, 15)},
        "SubLock4": {"CheckSubstat": (774, 531, 65, 13), "LockIcon": (1135, 541), "LockIconImage": (1130, 531, 15, 15)},
        "SubLock5": {"CheckSubstat": (774, 570, 64, 13), "LockIcon": (1135, 576), "LockIconImage": (1130, 570, 15, 15)},
        "SubLock6": {"CheckSubstat": (774, 609, 63, 13),  "LockIcon": (1135, 616), "LockIconImage": (1130, 609, 15, 15)},
        "SubLock7": {"CheckSubstat": (774, 646, 63, 17),  "LockIcon": (1135, 654), "LockIconImage": (1130, 645, 15, 15)}
    }

# --- PROFILE 161 (BẠN CẦN ĐIỀN TỌA ĐỘ MỚI VÀO ĐÂY) ---
class Layout_161:
    # Coordinates
    TARGET_SUBS = 6
    TOWER_ICON = (780, 340)
    MOD_ICON = (1000, 980)
    MOD_TO_ROLL_ICON = (1163, 601)

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
    TARGET_SUBS = 6
    TOWER_ICON = (780, 340)
    MOD_ICON = (1000, 980)
    MOD_TO_ROLL_ICON = MOD_LOCATION["Mod_2_2"]

    MOD_OPTIONS = (1087, 345)
    MOD_OPTIONS_DEBUG = (1089, 345)
    REROLL_EFFECTS = (1073, 388)
    AUTO_REROLL_BUTTON = (896, 729)
    VERIFICATION_BUTTON_YES = (1070, 670)
    EXIT_TOWER_BUTTON = (775, 14)
    MENU_BUTTON = (1790, 225)
    EMPTY_SPACE = (1400, 300)

    # Regions
    AUTO_REROLL_TEXT_REGION = (832, 715, 152, 26)
    LOADING_SCREEN_CHECK_REGION = (870, 680, 150, 70)

    # Substats Dictionary
    AFTER_ROLL_COORDS = {
        "exit_icon": (1140, 403),
        "check_icon": (1067, 909),
        "SubLock1": {"CheckSubstat": (774, 440, 64, 11), "LockIcon": (1135, 444), "LockIconImage": (1129, 436, 15, 15)},
        "SubLock2": {"CheckSubstat": (774, 476, 63, 15), "LockIcon": (1135, 484), "LockIconImage": (1129, 478, 15, 15)},
        "SubLock3": {"CheckSubstat": (774, 514, 63, 15), "LockIcon": (1135, 521), "LockIconImage": (1129, 514, 15, 15)},
        "SubLock4": {"CheckSubstat": (774, 553, 63, 15), "LockIcon": (1135, 561), "LockIconImage": (1129, 553, 15, 15)},
        "SubLock5": {"CheckSubstat": (774, 590, 66, 15), "LockIcon": (1135, 597), "LockIconImage": (1129, 590, 15, 15)},
        "SubLock6": {"CheckSubstat": (776, 628, 63, 15),  "LockIcon": (1135, 634), "LockIconImage": (1129, 628, 15, 15)}
    }

# --- PROFILE 241 (CẤU HÌNH HIỆN TẠI CỦA BẠN) ---
class Layout_241_with_bans:
    # Coordinates
    TARGET_SUBS = 7
    TOWER_ICON = (780, 340)
    MOD_ICON = (1000, 980)
    MOD_TO_ROLL_ICON = MOD_LOCATION["Core_ass"]

    MOD_OPTIONS = (1115, 330)
    MOD_OPTIONS_DEBUG = (1115, 320)
    REROLL_EFFECTS = (1100, 360)
    AUTO_REROLL_BUTTON = (910, 720)
    VERIFICATION_BUTTON_YES = (1070, 670)
    EXIT_TOWER_BUTTON = (775, 14)
    MENU_BUTTON = (1790, 225)
    EMPTY_SPACE = (1400, 300)

    # Regions
    AUTO_REROLL_TEXT_REGION = (831, 705, 147, 27)
    LOADING_SCREEN_CHECK_REGION = (870, 680, 150, 70)

    # Substats Dictionary
    AFTER_ROLL_COORDS = {
        "exit_icon": (1135, 350),
        "check_icon": (1070, 950),
        "SubLock1": {"CheckSubstat": (774, 389, 61, 13), "LockIcon": (1135, 399), "LockIconImage": (1130, 389, 15, 15)},
        "SubLock2": {"CheckSubstat": (774, 430, 61, 13), "LockIcon": (1135, 440), "LockIconImage": (1130, 430, 15, 15)},
        "SubLock3": {"CheckSubstat": (774, 467, 61, 13), "LockIcon": (1135, 475), "LockIconImage": (1130, 467, 15, 15)},
        "SubLock4": {"CheckSubstat": (774, 504, 65, 13), "LockIcon": (1135, 516), "LockIconImage": (1130, 504, 15, 15)},
        "SubLock5": {"CheckSubstat": (774, 541, 64, 13), "LockIcon": (1135, 553), "LockIconImage": (1130, 541, 15, 15)},
        "SubLock6": {"CheckSubstat": (774, 580, 63, 15),  "LockIcon": (1135, 588), "LockIconImage": (1130, 580, 15, 15)},
        "SubLock7": {"CheckSubstat": (774, 617, 63, 17),  "LockIcon": (1135, 626), "LockIconImage": (1130, 615, 15, 15)}
    }

# --- PROFILE 161 (BẠN CẦN ĐIỀN TỌA ĐỘ MỚI VÀO ĐÂY) ---
class Layout_161_with_bans:
    # Coordinates
    TARGET_SUBS = 6
    TOWER_ICON = (780, 340)
    MOD_ICON = (1000, 980)
    MOD_TO_ROLL_ICON = (1163, 601)

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
class Layout_201_with_bans:
    # Coordinates
    TARGET_SUBS = 7
    TOWER_ICON = (780, 340)
    MOD_ICON = (1000, 980)
    MOD_TO_ROLL_ICON = MOD_LOCATION["Mod_2_1"]

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
        "SubLock1": {"CheckSubstat": (772, 406, 68, 20), "LockIcon": (1135, 419), "LockIconImage": (1129, 406, 15, 15)},
        "SubLock2": {"CheckSubstat": (771, 445, 68, 20), "LockIcon": (1135, 459), "LockIconImage": (1129, 447, 15, 15)},
        "SubLock3": {"CheckSubstat": (772, 483, 68, 20), "LockIcon": (1135, 494), "LockIconImage": (1129, 483, 15, 15)},
        "SubLock4": {"CheckSubstat": (772, 524, 68, 17), "LockIcon": (1135, 534), "LockIconImage": (1129, 520, 15, 15)},
        "SubLock5": {"CheckSubstat": (772, 562, 68, 17), "LockIcon": (1135, 569), "LockIconImage": (1129, 559, 15, 15)},
        "SubLock6": {"CheckSubstat": (772, 598, 68, 20),  "LockIcon": (1135, 606), "LockIconImage": (1129, 598, 15, 15)},
        "SubLock7": {"CheckSubstat": (772, 638, 68, 17),  "LockIcon": (1135, 645), "LockIconImage": (1129, 637, 15, 15)}
    }
