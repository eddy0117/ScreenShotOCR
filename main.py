import os
import openai
import keyboard
import logging
import requests
from PyQt5.QtWidgets import QApplication
# from OCRapp.utils.config import load_config  
# from OCRapp.ui.ui import MainWindow 
# from OCRapp.ui.tray import create_tray  
# from OCRapp.core.ocr_process import process_clipboard_image  
# from OCRapp.utils.utils import apply_config_to_prompt
from OCRapp import utils
from OCRapp import ui
from OCRapp import core

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":

    config = utils.load_config()
    openai.api_key = config["api_key"]
    system_prompt = utils.apply_config_to_prompt(config)


    hotkey = config["hotkey"]
    logging.info(f"Waiting ({hotkey}) to trigger OCR...")
    keyboard.add_hotkey(hotkey, core.process_clipboard_image, args=(config, system_prompt))
    
    app = QApplication([])

    main_window = ui.MainWindow()

    main_window.show()
    tray = ui.create_tray(app, main_window)
    
    app.exec_()
