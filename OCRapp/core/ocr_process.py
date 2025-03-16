import io
import base64
import winsound
import pyperclip
from PIL import ImageGrab
import logging
from OCRapp.api import call_openai_api

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def process_clipboard_image(config: dict, system_prompt: str):
    img = ImageGrab.grabclipboard()
    if img is None:
        logging.error("No image in clipboard")
        winsound.MessageBeep(winsound.MB_ICONHAND)
        return
    buffer = io.BytesIO()
    img.resize((img.width // 3, img.height // 3))
    img = img.convert("RGB")
    img.save(buffer, format="JPEG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    extracted_text = call_openai_api(config, system_prompt, img_base64)
    if extracted_text is None:
        winsound.MessageBeep(winsound.MB_ICONHAND)
        return
    if extracted_text == "\"\"":
        logging.info("No text detected.")
    else:
        pyperclip.copy(extracted_text)
    logging.info("Text copied to clipboard.")
    winsound.MessageBeep()