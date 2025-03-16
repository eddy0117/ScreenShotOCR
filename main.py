
import openai
import keyboard
import logging
from PyQt5.QtWidgets import QApplication
from OCRapp.utils import load_config, apply_config_to_prompt
from OCRapp.ui import MainWindow, create_tray
from OCRapp.core import process_clipboard_image

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":

    config = load_config()
    openai.api_key = config["api_key"]
    system_prompt = apply_config_to_prompt(config)


    hotkey = config["hotkey"]
    logging.info(f"Waiting ({hotkey}) to trigger OCR...")
    keyboard.add_hotkey(hotkey, process_clipboard_image, args=(config, system_prompt))
    
    app = QApplication([])

    main_window = MainWindow()

    main_window.show()
    tray = create_tray(app, main_window)
    
    app.exec_()
