import cv2
from typing import Optional
from functions.yolo_api import YoloAPI, FrameResult

class CameraYoloAPI:
    """
    一个高级别的API，它封装了摄像头访问和YOLO实时推理。
    它接收一个已初始化的 YoloAPI 实例来进行推理。
    """
    def __init__(self, yolo_api: YoloAPI, source: int = 0):
        """
        初始化摄像头API实例，但不立即打开摄像头。

        Args:
            yolo_api (YoloAPI): 一个已经初始化好的 YoloAPI 实例。
            source (int): 摄像头ID。
        """
        if not isinstance(yolo_api, YoloAPI):
            raise TypeError("yolo_api 必须是一个 YoloAPI 的实例。")
        self.yolo = yolo_api
        self._source = source
        self.cap: Optional[cv2.VideoCapture] = None
        print(f"CameraYoloAPI 实例已创建，源: {self._source}，等待启动摄像头。")

    def start(self) -> bool:
        """
        尝试打开摄像头。如果已打开，则不执行任何操作。

        Returns:
            bool: 如果摄像头成功启动或已经运行，则返回 True；否则返回 False。
        """
        if self.cap and self.cap.isOpened():
            print(f"摄像头 {self._source} 已经运行。")
            return True

        try:
            self.cap = cv2.VideoCapture(self._source)
            if not self.cap.isOpened():
                raise RuntimeError(f"无法打开相机: {self._source}")
            print(f"摄像头 {self._source} 已成功启动。")
            return True
        except Exception as e:
            print(f"启动摄像头 {self._source} 失败: {e}")
            self.release() # 确保在启动失败时 cap 变为 None
            return False

    def stop(self):
        """
        停止并释放摄像头资源。
        """
        self.release()
        print(f"摄像头 {self._source} 已停止。")

    @property
    def is_active(self) -> bool:
        """
        检查摄像头是否正在运行。
        """
        return self.cap is not None and self.cap.isOpened()

    def process_next_frame(self, mirror_flip: bool = False) -> Optional[FrameResult]:
        """
        【核心接口】读取并处理下一帧，返回包含所有信息的字典。

        Returns:
            Optional[FrameResult]: 如果成功读取并推理，返回 FrameResult；否则返回 None。
        """
        if not self.is_active:
            # print(f"摄像头 {self._source} 未激活，无法处理帧。")
            return None

        ret, frame = self.cap.read()
        if not ret:
            print(f"无法从摄像头 {self._source} 读取帧。")
            return None

        if mirror_flip:
            frame = cv2.flip(frame, 1)

        # 直接调用 yolo_api 处理帧，并返回结果
        try:
            result = next(self.yolo.infer(frame))
            return result
        except StopIteration:
            print("YOLO推理生成器为空，可能没有检测到目标。")
            return {"raw_frame": frame, "boxes": [], "speed": {'preprocess': 0, 'inference': 0, 'postprocess': 0}} # 返回一个空结果
        except Exception as e:
            print(f"YOLO推理发生错误: {e}")
            return None # 返回None表示推理失败

    def release(self):
        """
        释放摄像头底层资源。
        """
        if self.cap and self.cap.isOpened():
            self.cap.release()
            print(f"摄像头 {self._source} 资源已释放。")
        self.cap = None