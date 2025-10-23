# yolo_api.py (已修复)

from pathlib import Path
from typing import Union, Iterator, List
import numpy as np
import cv2
from ultralytics import YOLO

DEFAULT_WEIGHT = "best.pt"
Box = List[float]
FrameResult = dict

# --- ↓↓↓ 核心修改点 1：定义合法的图片扩展名 ↓↓↓ ---
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}

class YoloAPI:
    _global_infer_log = False

    @classmethod
    def set_global_logging(cls, enable: bool):
        print(f"--- [Global Setting] YOLO API logging set to: {enable} ---")
        cls._global_infer_log = enable

    def __init__(self, weight: str = DEFAULT_WEIGHT, device: str = "cpu"):
        self.model = YOLO(weight)
        self.device = device

    def infer(self,
              source: Union[str, int, np.ndarray],
              conf: float = 0.25,
              iou: float = 0.45,
              mirror_flip: bool = False) -> Iterator[FrameResult]:

        # --- ↓↓↓ 核心修改点 2：重构逻辑顺序和判断条件 ↓↓↓ ---

        # 1. 首先处理路径类型 (字符串或Path对象)
        if isinstance(source, (str, Path)):
            p = Path(source)
            # 1a. 如果是目录，则按多图片处理
            if p.is_dir():
                if self.__class__._global_infer_log: print(f"[YOLO Log] Source: Directory -> {p}")
                for item in p.glob("*"):
                    if item.suffix.lower() in IMAGE_EXTENSIONS:
                        img = cv2.imread(str(item))
                        if img is not None:
                            yield self._predict_one(img, conf, iou)
                return

            # 1b. 如果是文件，则检查扩展名
            elif p.is_file():
                # 只处理图片文件
                if p.suffix.lower() in IMAGE_EXTENSIONS:
                    if self.__class__._global_infer_log: print(f"[YOLO Log] Source: Image File -> {p}")
                    img = cv2.imread(str(p))
                    if img is None: raise ValueError(f"图片读取失败: {p}")
                    yield self._predict_one(img, conf, iou)
                    return
                # 如果是其他类型的文件（如视频），则让它落到下面的 VideoCapture 处理
            else:
                raise FileNotFoundError(f"指定的路径不存在: {source}")

        # 2. 处理内存中的图像 (numpy 数组)
        if isinstance(source, np.ndarray):
            yield self._predict_one(source, conf, iou)
            return

        # 3. 最后，将所有剩下情况（摄像头ID、视频文件路径、RTSP流等）交给 VideoCapture
        cap = cv2.VideoCapture(source)
        if not cap.isOpened(): raise ValueError(f"视频/摄像头打开失败: {source}")
        if self.__class__._global_infer_log: print(f"[YOLO Log] Source: Stream -> {source}")
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    if self.__class__._global_infer_log: print("[YOLO Log] Stream ended.")
                    break
                if mirror_flip:
                    frame = cv2.flip(frame, 1)
                yield self._predict_one(frame, conf, iou)
        finally:
            cap.release()

    def _predict_one(self, bgr: np.ndarray, conf: float, iou: float) -> FrameResult:
        results = self.model.predict(bgr, conf=conf, iou=iou, device=self.device, verbose=False)
        r = results[0]
        if self.__class__._global_infer_log:
            log_message = f"    [Result] {r.verbose()}"
            print(log_message)
        boxes = []
        for b in r.boxes:
            x1, y1, x2, y2 = b.xyxy[0].tolist()
            boxes.append([x1, y1, x2, y2, b.conf[0].item(), int(b.cls[0].item())])
        annotated = r.plot()
        return {"frame": annotated, "boxes": boxes}

if __name__ == "__main__":
    print("正在运行 YoloAPI 单测...")
    YoloAPI.set_global_logging(True)
    try:
        api = YoloAPI(device="cpu")
        test_image = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(test_image, "Test Image", (200, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        print("\n--- [Test] 正在对一张测试图片进行推理 ---")
        res = next(api.infer(test_image))
        print("\n推理完成。显示结果图片，按任意键关闭。")
        cv2.imshow("YoloAPI Test", res["frame"])
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print("单测成功结束。")
    except Exception as e:
        print(f"单测失败: {e}")