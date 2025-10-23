# main.py
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton,
                               QVBoxLayout, QWidget, QStackedWidget, QSizePolicy)
from widgets.yolo_data_yaml.yolo_data_yaml import YoloDataYamlWidget
from widgets.display_train_info.view_combine import viewr_photo_csv

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("训练小工具集")
        self.resize(800, 600)

        # ---- 中心控件 ----
        central = QWidget()
        self.setCentralWidget(central)

        # 1. 垂直布局：内容区 + 按钮
        main_vlay = QVBoxLayout(central)
        main_vlay.setContentsMargins(5, 5, 5, 5)
        main_vlay.setSpacing(5)

        # 2. 上方内容区：QStackedWidget
        self.stack = QStackedWidget()
        main_vlay.addWidget(self.stack, stretch=1)   # stretch=1 占剩余全部空间

        # 3. 下方按钮：返回首页
        self.btn_home = QPushButton("返回首页")
        self.btn_home.setFixedHeight(40)             # 可选：固定高度
        main_vlay.addWidget(self.btn_home, stretch=0)  # stretch=0 不扩张

        # ---- 首页 ----
        home = QWidget()
        lay = QVBoxLayout(home)
        self.btn_yaml = QPushButton("YOLO data.yaml 生成器")
        self.btn_view = QPushButton("训练信息查看器")
        lay.addWidget(self.btn_yaml)
        lay.addWidget(self.btn_view)
        lay.addStretch()   # 把按钮挤到顶
        self.stack.addWidget(home)        # 0 号页面
        self.stack.setCurrentIndex(0)

        self.bind()

    def bind(self):
        self.btn_yaml.clicked.connect(self.show_yaml_widget)
        self.btn_view.clicked.connect(self.show_view_widget)
        self.btn_home.clicked.connect(self.go_home)

    # ---------- 原有逻辑 ----------
    def show_yaml_widget(self):
        if not hasattr(self, '_yaml_widget'):
            self._yaml_widget = YoloDataYamlWidget()
            self.stack.addWidget(self._yaml_widget)
        self.stack.setCurrentWidget(self._yaml_widget)

    def show_view_widget(self):
        if not hasattr(self, '_view_widget'):
            self._view_widget = viewr_photo_csv()
            self.stack.addWidget(self._view_widget)
        self.stack.setCurrentWidget(self._view_widget)

    def go_home(self):
        self.stack.setCurrentIndex(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())