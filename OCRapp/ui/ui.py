import logging
import os
import keyboard
import openai
from PyQt5.QtWidgets import QMainWindow, QWidget, QLineEdit, QLabel, QCheckBox, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QComboBox, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon 
from OCRapp.utils.config import load_config, save_config
from OCRapp.core.ocr_process import process_clipboard_image
from OCRapp.utils.utils import apply_config_to_prompt


class CustomComboBox(QComboBox):
    def __init__(self, items=None, parent=None):
        super().__init__(parent)
        if items:
            for item in items:
                if isinstance(item, tuple):
                    self.addItem(item[0], userData=item[1])
                else:
                    self.addItem(item)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowIcon(QIcon(os.path.join("OCRapp", "src", "icon.ico")))
        self.setWindowTitle("ScreenshotOCR settings")
        self.setMinimumSize(400, 250)
        self.config = load_config()
        self.init_ui()
    
    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        # API Key
        hlayout_api = QHBoxLayout()
        hlayout_api.addWidget(QLabel("API Key:"))
        self.api_entry = QLineEdit()
        self.api_entry.setEchoMode(QLineEdit.Password)
        self.api_entry.setText(self.config.get("api_key", ""))
        
        hlayout_api.addWidget(self.api_entry)
        layout.addLayout(hlayout_api)

        # Model list using CustomComboBox
        model_layout = QHBoxLayout()
        self.model_label = QLabel("model:")
        self.model_combo = CustomComboBox(
            [
                "gpt-4o", 
                "gpt-4o-mini"
             ])

        current_model = self.config["model"]
        idx = self.model_combo.findText(current_model)
        if idx != -1:
            self.model_combo.setCurrentIndex(idx)
        model_layout.addWidget(self.model_label)
        model_layout.addWidget(self.model_combo)
        layout.addLayout(model_layout)

        # Auto translate
        self.auto_translate_cb = QCheckBox("Enable auto translate")
        self.auto_translate_cb.setChecked(self.config.get("auto_translate", False))
        self.auto_translate_cb.toggled.connect(self.on_auto_translate_toggled)
        layout.addWidget(self.auto_translate_cb)

        lang_layout = QHBoxLayout()
        self.language_label = QLabel("Language:")
        self.language_combo = CustomComboBox(
            [
                ("Chinese (Traditional)", "zh-tw"),
                ("English", "en")
            ])

        current_lang = self.config.get("translate_language", "en")
        idx = self.language_combo.findData(current_lang)
        if idx != -1:
            self.language_combo.setCurrentIndex(idx)
        lang_layout.addWidget(self.language_label)
        lang_layout.addWidget(self.language_combo)
        layout.addLayout(lang_layout)

        # Hide combobox when auto translate is not checked
        self.language_label.setVisible(self.auto_translate_cb.isChecked())
        self.language_combo.setVisible(self.auto_translate_cb.isChecked())
        # Hot key config
        hlayout_hotkey = QHBoxLayout()
        hlayout_hotkey.addWidget(QLabel("Hot key:"))
        self.hotkey_entry = QLineEdit()
        self.hotkey_entry.setText(self.config.get("hotkey", "ctrl+alt+x"))
        hlayout_hotkey.addWidget(self.hotkey_entry)
        layout.addLayout(hlayout_hotkey)
        # Save btn
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_settings)
        layout.addWidget(self.save_btn)
        central.setLayout(layout)
    
    def on_auto_translate_toggled(self, checked):
        self.language_label.setVisible(checked)
        self.language_combo.setVisible(checked)
    
    def save_settings(self):
        # check if api key is empty
        if not self.api_entry.text().strip():
            QMessageBox.warning(self, "Warning", "API Key must be filled in!")
            return
        new_config = {
            "api_key": self.api_entry.text(),
            "model": self.model_combo.currentText(),
            "start_up": self.config.get("start_up", False),
            "auto_translate": self.auto_translate_cb.isChecked(),
            "translate_language": self.language_combo.currentData(),
            "hotkey": self.hotkey_entry.text()
        }
        save_config(new_config)
        openai.api_key = new_config["api_key"]
        self.statusBar().showMessage("Saved", 3000)
        self.apply_settings()
    
    def apply_settings(self):
        last_hotkey = self.config.get("hotkey")
        self.config = load_config()
        system_prompt = apply_config_to_prompt(self.config)
        keyboard.remove_hotkey(last_hotkey)
        keyboard.add_hotkey(self.config.get("hotkey"), process_clipboard_image, args=(self.config, system_prompt ))

    def closeEvent(self, event):
        event.accept()
        QApplication.quit()
    
    # Hide window when clicking minimize
    def changeEvent(self, event):
        from PyQt5.QtCore import QEvent
        if event.type() == QEvent.WindowStateChange:
            if self.isMinimized():
                QTimer.singleShot(0, self.hide)
        super(MainWindow, self).changeEvent(event)