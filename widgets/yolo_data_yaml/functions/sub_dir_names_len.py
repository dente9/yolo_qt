from pathlib import Path

def get_subfolders(folder_path):
    """
    接受一个文件夹地址，返回其下一级目录的子文件夹数量和子文件夹名字。

    参数:
    folder_path (str): 文件夹的路径

    返回:
    tuple: (子文件夹数量, 子文件夹名字列表)
    """
    folder = Path(folder_path)  # 将路径字符串转换为 Path 对象
    if not folder.is_dir():  # 检查路径是否是一个目录
        raise ValueError(f"{folder_path} 不是一个有效的目录")

    subfolders = [item for item in folder.iterdir() if item.is_dir()]  # 获取所有子文件夹
    subfolder_names = [subfolder.name for subfolder in subfolders]  # 获取子文件夹的名字
    subfolder_count = len(subfolders)  # 子文件夹的数量

    return (subfolder_count, subfolder_names)

# 示例用法
if __name__ == "__main__":
    folder_path = input("请输入文件夹路径: ")
    try:
        subfolder_count, subfolder_names = get_subfolders(folder_path)
        print(f"子文件夹数量: {subfolder_count}")
        print(f"子文件夹名字: {subfolder_names}")
    except ValueError as e:
        print(e)