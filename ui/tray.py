import os
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QMainWindow
from PyQt5.QtGui import QIcon


def create_tray(app, window: QMainWindow):
    icon_path = os.path.join("src", "icon.ico")
    tray = QSystemTrayIcon(QIcon(icon_path), app)

    menu = QMenu(window)
    action_show = QAction("Settings", window)
    action_close = QAction("Exit", window)
    menu.addAction(action_show)
    menu.addAction(action_close)
    tray.setContextMenu(menu)

    tray.menu = menu
    action_show.triggered.connect(window.show)
    action_close.triggered.connect(app.quit)
    tray.activated.connect(lambda reason:
                             window.show() if reason == QSystemTrayIcon.DoubleClick else None)
    tray.show()
    return tray
