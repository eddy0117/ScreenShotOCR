import os
import openai
import keyboard
import logging
import requests
from PyQt5.QtWidgets import QApplication
from utils.config import load_config  
from ui.ui import MainWindow 
from ui.tray import create_tray  
from core.ocr_process import process_clipboard_image  
from utils.utils import apply_config_to_prompt
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
