# camera_yolo_api.py

import cv2
import traceback
import numpy as np
from typing import Optional, Tuple

# 假设 yolo_api.py 和这个文件在同一个目录下
from yolo_api import YoloAPI, FrameResult


class CameraYoloAPI:
    """
    一个高级别的API，它封装了摄像头访问和YOLO实时推理。
    这个类的设计是为了逐帧处理，非常适合集成到像Qt这样的GUI应用程序中。

    Qt中的典型用法:
    1. 在窗口初始化时:
       self.camera_api = CameraYoloAPI(source=0)
    2. 创建一个 QTimer:
       self.timer = QTimer(self)
       self.timer.timeout.connect(self.update_frame)
       self.timer.start(30)  # 每30毫秒请求一帧
    3. 在 update_frame 方法中:
       result = self.camera_api.process_next_frame(mirror_flip=True)
       if result:
           # 将 result["frame"] (BGR图像) 转换为QImage并显示在QLabel上
           ...
    4. 在关闭窗口时:
       self.camera_api.release()
    """

    def __init__(self,
                 source: int | str = 0,
                 resolution: Optional[Tuple[int, int]] = (640, 480),
                 yolo_weight: str = "best.pt",
                 device: str = "cpu"):
        """
        初始化摄像头和YOLO模型。

        Args:
            source (int | str): 摄像头ID或视频文件路径。
            resolution (Optional[Tuple[int, int]]): 摄像头分辨率 (宽, 高)。
            yolo_weight (str): YOLO模型权重文件路径。
            device (str): 推理设备 ("cpu", "cuda", etc.)。
        """
        try:
            # 1. 初始化YOLO推理引擎
            self.yolo = YoloAPI(weight=yolo_weight, device=device)

            # 2. 初始化视频捕捉
            self.cap = cv2.VideoCapture(source)
            if not self.cap.isOpened():
                raise RuntimeError(f"无法打开相机/视频: {source}")

            # 仅对USB相机设置分辨率
            if isinstance(source, int) and resolution:
                w, h = resolution
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

            self.is_running = True
            print("CameraYoloAPI 初始化成功。")

        except Exception as e:
            self.is_running = False
            self.cap = None
            print(f"CameraYoloAPI 初始化失败: {e}")
            raise

    def process_next_frame(self, mirror_flip: bool = False) -> Optional[FrameResult]:
        """
        【核心接口】读取并处理下一帧。
        这是非阻塞的，设计用来被外部循环（如QTimer）调用。

        Args:
            mirror_flip (bool): 是否对画面进行镜像翻转。

        Returns:
            Optional[FrameResult]: 一个包含处理后图像和检测框的字典，
                                   如果视频结束或读取失败则返回 None。
        """
        if not self.is_running or not self.cap.isOpened():
            return None

        ret, frame = self.cap.read()
        if not ret:
            self.is_running = False  # 视频结束或摄像头掉线
            return None

        # yolo.infer() 本身就是在处理单帧，我们直接调用即可
        # 注意：这里的yolo.infer(frame)返回的是一个只yield一次的生成器
        result = next(self.yolo.infer(frame, mirror_flip=mirror_flip))

        return result

    def release(self):
        """
        释放摄像头资源。在应用程序关闭时必须调用。
        """
        if self.cap and self.cap.isOpened():
            self.cap.release()
            print("摄像头资源已释放。")
        self.is_running = False


# --------- 使用示例和测试 ---------
def run_test():

    try:
        YoloAPI.set_global_logging(True)
        yolo = YoloAPI(device="cpu")

        camera_source = 0


        for res in yolo.infer(camera_source, mirror_flip=True):

            vis_frame = res["frame"]


            cv2.imshow("YOLO-Camera  (ESC 退出)", vis_frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break

        cv2.destroyAllWindows()

    except Exception as e:
        print("程序发生错误！")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {e}")
        print("详细追溯信息:")
        traceback.print_exc()
        input("按 Enter 键退出...")


if __name__ == "__main__":
    run_test()