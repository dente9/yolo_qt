from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class PhotoViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._label = QLabel(alignment=Qt.AlignCenter)
        self._label.setScaledContents(True)
        self._label.setStyleSheet("QLabel{background-color:black;color:white;}")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self._label)

    def load(self, path: Path):
        pix = QPixmap(str(path))
        if not pix.isNull():
            self._label.setPixmap(pix.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))