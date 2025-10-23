# test.py

import cv2
import numpy as np
from pathlib import Path
import time

# 确保 yolo_api.py 在同一个目录下
from yolo_api import YoloAPI

# --- 全局配置 ---
# 测试素材将被创建在这个文件夹下
ASSETS_DIR = Path("test_assets")
IMAGE_SUBDIR = ASSETS_DIR / "images"
VIDEO_PATH = ASSETS_DIR / "sample_video.mp4"
SINGLE_IMAGE_PATH = IMAGE_SUBDIR / "test_image_01.jpg"

def setup_test_environment():
    """自动创建用于测试的图片和视频文件。"""
    print("--- 检查并创建测试素材 ---")
    try:
        # 创建主目录和图片子目录
        ASSETS_DIR.mkdir(exist_ok=True)
        IMAGE_SUBDIR.mkdir(exist_ok=True)

        # 1. 创建测试图片
        if not (IMAGE_SUBDIR / "test_image_02.jpg").exists():
            print(f"正在创建测试图片到 '{IMAGE_SUBDIR}'...")
            for i in range(1, 3):
                img = np.zeros((480, 640, 3), dtype=np.uint8)
                text = f"Test Image {i:02d}"
                cv2.putText(img, text, (180, 240), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
                cv2.imwrite(str(IMAGE_SUBDIR / f"test_image_{i:02d}.jpg"), img)
            print("图片创建完成。")
        else:
            print("测试图片已存在。")

        # 2. 创建测试视频
        if not VIDEO_PATH.exists():
            print(f"正在创建测试视频 '{VIDEO_PATH}'...")
            width, height = 640, 480
            fps = 20
            duration_sec = 5
            # 使用 'mp4v' 编码器，兼容性好
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(str(VIDEO_PATH), fourcc, fps, (width, height))

            for i in range(fps * duration_sec):
                frame = np.zeros((height, width, 3), dtype=np.uint8)
                text = f"Frame: {i+1}"
                # 移动的圆
                cx = int(width / 2 + 100 * np.sin(2 * np.pi * i / (fps * 2)))
                cy = int(height / 2 + 100 * np.cos(2 * np.pi * i / (fps * 2)))
                cv2.circle(frame, (cx, cy), 30, (0, 255, 0), -1)
                cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                writer.write(frame)
            writer.release()
            print("视频创建完成。")
        else:
            print("测试视频已存在。")

    except Exception as e:
        print(f"\n[错误] 创建测试素材失败: {e}")
        print("请检查文件夹权限或依赖库(OpenCV, NumPy)。")
        exit()
    print("-" * 28 + "\n")


def test_single_image(api: YoloAPI):
    """测试对单张图片文件的推理。"""
    print(f"\n--- 测试 1: 单张图片 ---")
    print(f"输入: {SINGLE_IMAGE_PATH}")
    print("按任意键关闭图片窗口。")
    for result in api.infer(str(SINGLE_IMAGE_PATH)):
        cv2.imshow("Test 1: Single Image", result["frame"])
        cv2.waitKey(0)
    cv2.destroyAllWindows()


def test_image_folder(api: YoloAPI):
    """测试对图片文件夹（多图片）的推理。"""
    print(f"\n--- 测试 2: 图片文件夹 ---")
    print(f"输入: {IMAGE_SUBDIR}")
    print("将逐一显示结果，每次按任意键切换到下一张。")
    for i, result in enumerate(api.infer(str(IMAGE_SUBDIR))):
        window_name = f"Test 2: Image Folder (Image {i+1})"
        cv2.imshow(window_name, result["frame"])
        if cv2.waitKey(0) == 27: # 按 ESC 可提前退出
            break
    cv2.destroyAllWindows()


def test_video_file(api: YoloAPI):
    """测试对视频文件的推理。"""
    print(f"\n--- 测试 3: 视频文件 ---")
    print(f"输入: {VIDEO_PATH}")
    print("正在播放视频... 按 'ESC' 键可提前退出。")
    for result in api.infer(str(VIDEO_PATH)):
        cv2.imshow("Test 3: Video File", result["frame"])
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cv2.destroyAllWindows()


def test_live_camera(api: YoloAPI):
    """测试对摄像头的实时推理。"""
    print(f"\n--- 测试 4: 实时摄像头 ---")
    print("输入: 摄像头 0")
    print("正在打开摄像头... 按 'ESC' 键退出。")
    # 摄像头使用镜像翻转更符合直觉
    for result in api.infer(0, mirror_flip=True):
        cv2.imshow("Test 4: Live Camera", result["frame"])
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cv2.destroyAllWindows()


def main():
    """主函数，提供交互式菜单来运行所有测试。"""

    # 自动创建测试文件
    setup_test_environment()

    # 在程序顶层设置全局日志开关
    YoloAPI.set_global_logging(True)

    try:
        # 初始化YOLO API
        api = YoloAPI(device="cpu")
    except Exception as e:
        print(f"\n[致命错误] 初始化 YoloAPI 失败: {e}")
        print("请确保 'best.pt' 模型文件在当前目录下。")
        input("按 Enter 键退出...")
        return

    while True:
        print("\n" + "="*15 + " YoloAPI 测试菜单 " + "="*15)
        print("1. 测试单张图片推理")
        print("2. 测试图片文件夹（多图片）推理")
        print("3. 测试视频文件推理")
        print("4. 测试实时摄像头推理")
        print("5. 退出")
        print("="*48)

        choice = input("请输入你的选择 (1-5): ")

        if choice == '1':
            test_single_image(api)
        elif choice == '2':
            test_image_folder(api)
        elif choice == '3':
            test_video_file(api)
        elif choice == '4':
            test_live_camera(api)
        elif choice == '5':
            print("测试结束，再见！")
            break
        else:
            print("无效输入，请输入 1 到 5 之间的数字。")

        time.sleep(1) # 暂停一下，给用户看清上次测试的结束信息


if __name__ == "__main__":
    main()