"""image_ocr.py - Optional OCR support for image files."""
from pathlib import Path

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
_COMMON_WINDOWS_PATHS = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
]

def is_image(path):
    return Path(path).suffix.lower() in IMAGE_EXTENSIONS

def ocr_image(path):
    try:
        import pytesseract
        from PIL import Image
    except ImportError:
        return None
    try:
        img = Image.open(path)
    except Exception:
        return None
    try:
        text = pytesseract.image_to_string(img).strip()
        if text:
            return text
    except Exception:
        pass
    for candidate in _COMMON_WINDOWS_PATHS:
        if Path(candidate).exists():
            pytesseract.pytesseract.tesseract_cmd = candidate
            try:
                text = pytesseract.image_to_string(img).strip()
                if text:
                    return text
            except Exception:
                continue
    return None
