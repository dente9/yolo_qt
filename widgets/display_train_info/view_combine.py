#!/usr/bin/env python
import sys
from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QPushButton, QFileDialog)

from .photo_viewer import PhotoViewer
from .csv_view import CsvViewer

class viewr_photo_csv(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("图片 / CSV 浏览器")
        self.resize(900, 700)

        # ---- 中央控件 ----
        central = QWidget()
        self.setCentralWidget(central)
        vlay = QVBoxLayout(central)
        vlay.setContentsMargins(5, 5, 5, 5)

        # 两个 viewer 叠在一起
        self._photo = PhotoViewer()
        self._csv = CsvViewer()
        vlay.addWidget(self._photo, stretch=1)
        vlay.addWidget(self._csv, stretch=1)

        # 按钮栏
        hlay = QHBoxLayout()
        self._btn_open = QPushButton("打开文件夹")
        self._btn_prev = QPushButton("上一个 (←)")
        self._btn_next = QPushButton("下一个 (→)")
        hlay.addWidget(self._btn_open)
        hlay.addStretch()
        hlay.addWidget(self._btn_prev)
        hlay.addWidget(self._btn_next)

        vlay.addLayout(hlay)

        # 数据
        self._folder: Path | None = None
        self._files: list[Path] = []
        self._idx = -1

        # 初始状态：未选文件夹 -> 默认显示图片控件（空）
        self._csv.setVisible(False)
        self._photo.setVisible(True)
        self.setWindowTitle("请选择文件夹")



        self.bind()
    def bind(self):
        self._btn_open.clicked.connect(self.open_folder)
        self._btn_prev.clicked.connect(self.prev_file)
        self._btn_next.clicked.connect(self.next_file)
        # 键盘
        self.setFocusPolicy(Qt.StrongFocus)


    # ---------- 逻辑 ----------
    def open_folder(self):
        dir_ = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if not dir_:
            return
        self._folder = Path(dir_)
        suffix = {'.jpg', '.jpeg', '.png', '.bmp', '.csv'}
        self._files = sorted([p for p in self._folder.iterdir() if p.suffix.lower() in suffix])
        self._idx = 0 if self._files else -1
        self.show_current()

    def show_current(self):
        if not (0 <= self._idx < len(self._files)):
            self._photo.setVisible(False)
            self._csv.setVisible(False)
            self.setWindowTitle("无文件")
            return

        path = self._files[self._idx]
        self.setWindowTitle(f"{path.name}  –  {self._idx + 1}/{len(self._files)}")

        if path.suffix.lower() == '.csv':
            self._photo.setVisible(False)
            self._csv.setVisible(True)
            self._csv.load(path)
        else:  # image
            self._csv.setVisible(False)
            self._photo.setVisible(True)
            self._photo.load(path)

    def prev_file(self):
        if self._files:
            self._idx = (self._idx - 1) % len(self._files)
            self.show_current()

    def next_file(self):
        if self._files:
            self._idx = (self._idx + 1) % len(self._files)
            self.show_current()

    # ---------- 键盘 ----------
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Left:
            self.prev_file()
        elif event.key() == Qt.Key_Right:
            self.next_file()
        else:
            super().keyPressEvent(event)

    # ---------- 滚轮 ----------
    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if delta > 0:
            self.prev_file()
        else:
            self.next_file()

# -------------------- main --------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = viewr_photo_csv()
    w.show()
    sys.exit(app.exec())