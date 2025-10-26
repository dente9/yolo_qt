import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'widgets', 'display_apply'))

from display_apply import BgMainWindow, DisplayApp
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DisplayApp()
    window = BgMainWindow(window)
    window.show()
    sys.exit(app.exec())