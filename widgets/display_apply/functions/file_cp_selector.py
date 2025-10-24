import os
import shutil
from PySide6.QtWidgets import QFileDialog

def open_selector(parent_widget, target_folder, file_or_dir='file',label_widget=None):
    """
    打开文件或文件夹选择对话框，选择文件或文件夹并复制到目标文件夹。
    如果所选文件/文件夹已在目标位置，则不执行复制。

    :param parent_widget: 父窗口部件
    :param label_widget: 用于显示文件路径的 QLabel
    :param target_folder: 目标文件夹路径 (可以是 str 或 pathlib.Path 对象)
    :param file_or_dir: 'file' 或 'dir'，决定打开文件选择器还是文件夹选择器
    :return: 最终在目标文件夹中的文件/文件夹的路径，如果用户取消则返回 None
    """
    selected_path_in_target = None

    # 确保 target_folder 是字符串，以兼容 os.path 和 QFileDialog
    target_folder_str = str(target_folder)

    if file_or_dir == 'file':
        # 打开文件选择对话框，起始目录为目标文件夹
        file_path, _ = QFileDialog.getOpenFileName(parent_widget, "选择文件", target_folder_str, "All Files (*)")

        if file_path:
            # 如果目标文件夹不存在，则创建它
            if not os.path.exists(target_folder_str):
                os.makedirs(target_folder_str)

            # 定义目标文件路径
            target_file_path = os.path.join(target_folder_str, os.path.basename(file_path))

            # 检查源文件和目标文件是否是同一个文件
            try:
                # os.path.samefile() 会准确地判断两个路径是否指向同一个文件
                is_same = os.path.samefile(file_path, target_file_path)
            except FileNotFoundError:
                # 如果 target_file_path 还不存在，说明肯定不是同一个文件
                is_same = False

            if not is_same:
                # 如果不是同一个文件，则执行复制
                shutil.copy(file_path, target_file_path)
                print(f"文件已复制到: {target_file_path}")
            else:
                # 如果是同一个文件，则跳过复制
                print("所选文件已在目标文件夹中，无需复制。")

            # 无论是否复制，都将目标路径赋给返回值
            selected_path_in_target = target_file_path

    elif file_or_dir == 'dir':
        # 打开文件夹选择对话框，起始目录为目标文件夹的父目录
        parent_dir = os.path.dirname(target_folder_str)
        dir_path = QFileDialog.getExistingDirectory(parent_widget, "选择文件夹", parent_dir)

        if dir_path:
            if not os.path.exists(target_folder_str):
                os.makedirs(target_folder_str)

            target_dir_path = os.path.join(target_folder_str, os.path.basename(dir_path))

            # 使用 os.path.abspath 规范化路径以进行比较
            if os.path.abspath(dir_path) != os.path.abspath(target_dir_path):
                # 如果目标已存在，先删除再复制 (注意: 这会覆盖!)
                if os.path.exists(target_dir_path):
                   shutil.rmtree(target_dir_path)
                shutil.copytree(dir_path, target_dir_path)
                print(f"文件夹已复制到: {target_dir_path}")
            else:
                print("所选文件夹已在目标位置，无需复制。")

            selected_path_in_target = target_dir_path
    else:
        raise ValueError("file_or_dir 参数必须是 'file' 或 'dir'")

    # 如果成功选择了路径，更新UI标签
    if selected_path_in_target and label_widget:
        label_widget.setText(selected_path_in_target)

    # 返回最终在目标文件夹中的路径
    return selected_path_in_target