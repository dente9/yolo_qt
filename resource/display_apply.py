import sys
import os
from PySide6.QtWidgets import QApplication, QWidget
from Ui_display import Ui_Form  # 假设你的UI类名为 Ui_Form
from functions.file_cp_selector import open_selector

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_root)
from config import MODEL_STORE_PATH, INPUT_FILE_PATH  # 注意拼写错误，应该是 MODEL_SAVE_PATH

class DisplayApp(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.bind()

    def bind(self):
        # 绑定按钮点击事件，选择文件
        self.ui.btn_model_select.clicked.connect(lambda: self.handle_file_selection(MODEL_STORE_PATH, 'file'))
        self.ui.btn_open_one_file.clicked.connect(lambda: self.handle_file_selection(INPUT_FILE_PATH, 'file'))
        # 绑定按钮点击事件，选择文件夹
        self.ui.btn_open_dir.clicked.connect(lambda: self.handle_file_selection(INPUT_FILE_PATH, 'dir'))

    def handle_file_selection(self, target_folder, file_or_dir):
        selected_path = open_selector(self, self.ui.lb_info_file_path, target_folder, file_or_dir)
        if selected_path:
            # 在这里处理选择的文件或文件夹路径
            print(f"选择的路径: {selected_path}")
            # 你可以在 self.ui.display 中显示一些内容
            self.ui.display.setText(f"选择的路径: {selected_path}")
            # 你可以在这里添加更多的逻辑，例如处理视频等

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DisplayApp()
    window.show()
    sys.exit(app.exec())