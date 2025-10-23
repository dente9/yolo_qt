import sys
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from .Ui_main import Ui_Form  # 导入你编译生成的 Ui_Form 类
from functions.sub_dir_names_len import get_subfolders  # 导入 get_subfolders 函数
from pathlib import Path
import yaml

results={"data_path":"", "class_num":0, "class_name":""}


class YoloDataYamlWidget(QWidget):

    def __init__(self):
        self.yaml_content=""
        super().__init__()
        self.ui = Ui_Form()  # 创建 Ui_Form 类的实例
        self.ui.setupUi(self)  # 设置 UI
        self.ui.lb_show
        self.bind()  # 绑定事件

    def bind(self):
        self.ui.pb_get_len_names.clicked.connect(self.get_subfolders)  # 绑定按钮点击事件
        self.ui.pb_get_path.clicked.connect(self.get_folder_path)
        self.ui.le_path.textChanged.connect(self.update_results)
        self.ui.le_class_num.textChanged.connect(self.update_results)
        self.ui.le_class_name.textChanged.connect(self.update_results)
        self.ui.pb_save.clicked.connect(self.save_yaml)



    def get_folder_path(self):
        # 获取当前文件夹路径
        folder_path = self.ui.le_path.text()
        # 打开文件夹选择对话框
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹", folder_path)
        if folder_path:  # 如果用户选择了文件夹
            # 将选择的文件夹路径设置到 QLineEdit 中
            self.ui.le_path.setText(folder_path)
            results["data_path"] = folder_path
            self.show_info()


    def get_subfolders(self):
        # 打开文件夹选择对话框
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder_path:  # 如果用户选择了文件夹
            try:
                # 调用 get_subfolders 函数获取子文件夹数量和名字
                subfolder_count, subfolder_names = get_subfolders(folder_path)
                # 将结果设置到对应的 QLineEdit 中
                self.ui.le_class_num.setText(str(subfolder_count))
                self.ui.le_class_name.setText(", ".join(subfolder_names))
                results["class_num"] = str(subfolder_count)
                results["class_name"] = subfolder_names
                self.show_info()
            except Exception as e:
                # 如果发生错误，显示错误信息
                self.ui.le_class_num.setText("错误")
                self.ui.le_class_name.setText(str(e))

    def show_info(self):
        data_path = Path(results["data_path"])
        self.yaml_dict = {
            "train": str(data_path / "train"),
            "val":   str(data_path / "val"),
            "test":  str(data_path / "test"),
            "nc":    int(results["class_num"]) if results["class_num"].isdigit() else 0,
            "names": [s for s in results["class_name"]]
        }
        self.yaml_content = yaml.dump(self.yaml_dict, sort_keys=False, allow_unicode=True)
        self.ui.lb_show.setText(self.yaml_content)


    def update_results(self):
        # 更新 results 字典
        results["data_path"] = self.ui.le_path.text()
        results["class_num"] = self.ui.le_class_num.text()
        results["class_name"] = [line.strip() for line in self.ui.le_class_name.toPlainText().splitlines()
                                    if line.strip()]
        self.show_info()

    def save_yaml(self):
        if not self.yaml_content:
            return
        path = Path(results["data_path"]) / "data.yaml"
        path.write_text(self.yaml_content, encoding="utf-8")
        self.ui.lb_show.setText(f"已保存 -> {path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建应用程序实例
    window = YoloDataYamlWidget()  # 创建主窗口实例
    window.show()  # 显示主窗口
    sys.exit(app.exec())  # 运行应用程序并等待退出