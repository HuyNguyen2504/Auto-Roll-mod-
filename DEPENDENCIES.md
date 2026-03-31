# Dependencies Configuration

This document outlines all libraries and dependencies used in the Silver AutoReroll project.

## External Libraries

### Core Automation & GUI
- **pyautogui** (v0.9.53) - Mouse and keyboard automation
- **pydirectinput** (v1.0.4) - Direct input simulation for games
- **keyboard** (v0.13.5) - Keyboard event handling

### GUI Frameworks
- **customtkinter** (v5.2.0) - Modern Tkinter wrapper for beautiful UI
- **PyQt5** (v5.15.9) - Qt5 bindings for Python GUI applications
- **Pillow** (v10.1.0) - Python Imaging Library for image processing

### Computer Vision & OCR
- **opencv-python** (v4.8.1.78) - Computer vision library (cv2)
- **pytesseract** (v0.3.10) - Python wrapper for Tesseract OCR
- **numpy** (v1.24.3) - Numerical computing library (used by OpenCV)

### Utilities
- **requests** (v2.31.0) - HTTP library for API calls (Bark notifications)
- **python-dotenv** (v1.0.0) - Environment variable management

## System Dependencies

### External Tools
- **Tesseract-OCR** - Required for text recognition
  - Installation path: `C:\Program Files\Tesseract-OCR\tesseract.exe`
  - Configure in `.env` file with `TESSERACT_PATH` variable

### API Services
- **Bark** - iPhone push notification service
  - Device key stored in `.env` as `BARK_KEY`

## Installation

### Using requirements.txt
```bash
pip install -r requirements.txt
```

### Using pyproject.toml
```bash
pip install -e .
```

### With Development Dependencies
```bash
pip install -e ".[dev]"
```

## Module Usage by File

| File | Key Libraries |
|------|---------------|
| `reroll.py` | pyautogui, pytesseract, opencv-python, numpy, requests |
| `reroll_UI.py` | customtkinter, threading |
| `calibration.py` | pyautogui, opencv-python, pytesseract, pydirectinput, requests |
| `calibrationUI.py` | PyQt5, sqlite3, keyboard, pyautogui |
| `variable.py` | python-dotenv |

## Environment Variables

Create a `.env` file with the following:
```
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
BARK_KEY=your_device_key_here
```

## Notes

- Python 3.8+ is required
- OpenCV and NumPy are computationally intensive; ensure sufficient system resources
- Tesseract-OCR must be installed separately and path configured in `.env`
- Some modules require admin privileges to function properly (keyboard, pydirectinput)
