# functions/yolo_api.py (增强后)

from pathlib import Path
from typing import Union, Iterator, List, Optional, Dict
import numpy as np
import cv2
from ultralytics import YOLO

# 定义更详细的返回类型
Box = List[Union[float, int, str]] # [x1, y1, x2, y2, conf, cls_id, cls_name]
FrameResult = Dict[str, Union[np.ndarray, List[Box], Dict, None]]
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}

class YoloAPI:
    _global_infer_log = False

    @classmethod
    def set_global_logging(cls, enable: bool):
        print(f"--- [Global Setting] YOLO API logging set to: {enable} ---")
        cls._global_infer_log = enable

    @staticmethod
    def create_instance(model_path: Union[str, Path], device: str = "cpu") -> Optional['YoloAPI']:
        model_file = Path(model_path)
        if not model_file.is_file():
            print(f"错误：模型文件不存在或不是一个文件: {model_file}")
            return None
        try:
            print(f"正在从 {model_file.name} 加载YOLO模型...")
            instance = YoloAPI(weight=str(model_file), device=device)
            print("YOLO模型加载成功！")
            return instance
        except Exception as e:
            print(f"错误：YOLO模型初始化失败！ {e}")
            return None

    def __init__(self, weight: str, device: str = "cpu"):
        self.model = YOLO(weight)
        self.device = device
        # ✅ 获取模型所有类别的名称
        self.class_names = self.model.names

    def infer(self, source: Union[str, int, np.ndarray], conf: float = 0.25, iou: float = 0.45) -> Iterator[FrameResult]:
        # 注意：为了简化，这里的 mirror_flip 逻辑移到了主程序中
        # ... infer 方法的其他部分保持不变 ...
        if isinstance(source, np.ndarray):
            yield self._predict_one(source, conf, iou)
            return

        # 其他 source 类型的处理逻辑...
        is_stream = False
        if isinstance(source, (str, Path)):
            p = Path(source)
            if p.is_dir():
                # ... 目录处理逻辑
                return
            elif p.is_file():
                if p.suffix.lower() not in IMAGE_EXTENSIONS:
                    is_stream = True
            else:
                 if not (isinstance(source, int) or "rtsp://" in str(source)):
                     raise FileNotFoundError(f"指定的路径不存在: {source}")

        if isinstance(source, int) or is_stream:
            cap = cv2.VideoCapture(source)
            if not cap.isOpened(): raise ValueError(f"视频/摄像头打开失败: {source}")
            try:
                while True:
                    ret, frame = cap.read()
                    if not ret: break
                    yield self._predict_one(frame, conf, iou)
            finally:
                cap.release()
        else: # 单张图片
             img_array = np.fromfile(source, dtype=np.uint8)
             img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
             if img is None: raise ValueError(f"图片读取失败: {source}")
             yield self._predict_one(img, conf, iou)

    # ✅ --- 核心修改：_predict_one 返回更丰富的数据 ---
    def _predict_one(self, bgr: np.ndarray, conf: float, iou: float) -> FrameResult:
        """
        对单帧图像进行预测，并返回一个包含所有详细信息的字典。
        """
        results = self.model.predict(bgr, conf=conf, iou=iou, device=self.device, verbose=False)
        r = results[0]

        # 1. 提取详细的 boxes 信息
        detailed_boxes = []
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            cls_id = int(box.cls[0].item())
            cls_name = self.class_names[cls_id]
            confidence = box.conf[0].item()
            detailed_boxes.append([x1, y1, x2, y2, confidence, cls_id, cls_name])

        # 2. 提取处理速度
        speed = r.speed  # 这是一个字典, e.g., {'preprocess': 1.0, 'inference': 2.0, 'postprocess': 3.0}

        if self.__class__._global_infer_log:
            print(f"    [Result] {r.verbose()}")

        # 3. 返回包含所有信息的字典
        return {
            "raw_frame": bgr,  # 未经修改的原始帧
            "annotated_frame": r.plot(), # 画了所有框的帧
            "boxes": detailed_boxes, # 结构化的检测框数据
            "speed": speed # 推理速度
        }