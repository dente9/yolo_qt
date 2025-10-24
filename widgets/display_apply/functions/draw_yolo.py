# functions/draw_yolo.py

from typing import List, Optional
import numpy as np
import cv2
from functions.yolo_api import Box # 导入我们定义的Box类型

# 定义颜色和字体，方便统一修改
COLOR_GREEN = (0, 255, 0)
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.7
FONT_THICKNESS = 2
BOX_THICKNESS = 2

def _draw_single_box(frame: np.ndarray, box: Box):
    """一个在图像上绘制单个边界框的辅助函数。"""
    x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
    confidence = box[4]
    class_name = box[6]

    label = f"{class_name} {confidence:.2f}"

    # 绘制边界框
    cv2.rectangle(frame, (x1, y1), (x2, y2), COLOR_GREEN, BOX_THICKNESS)

    # 绘制标签背景
    (w, h), _ = cv2.getTextSize(label, FONT, FONT_SCALE, FONT_THICKNESS)
    cv2.rectangle(frame, (x1, y1 - h - 5), (x1 + w, y1), COLOR_GREEN, -1)

    # 绘制标签文字
    cv2.putText(frame, label, (x1, y1 - 5), FONT, FONT_SCALE, (0, 0, 0), FONT_THICKNESS)


def draw_boxes(
    raw_frame: np.ndarray,
    all_boxes: List[Box],
    target_index: Optional[int] = None
) -> np.ndarray:
    """
    根据选择在原始帧上绘制边界框。

    Args:
        raw_frame (np.ndarray): 未经修改的原始 BGR 图像。
        all_boxes (List[Box]): 当前帧检测到的所有目标的列表。
        target_index (Optional[int]):
            - 如果是 None, 则绘制所有目标的边界框。
            - 如果是整数 (e.g., 0, 1, 2...), 则只绘制该索引对应的目标。

    Returns:
        np.ndarray: 绘制了所需边界框的新图像。
    """
    frame_to_draw = raw_frame.copy()

    if not all_boxes:
        return frame_to_draw # 如果没有检测框，直接返回原图副本

    if target_index is None:
        # "All" 模式：绘制所有框
        for box in all_boxes:
            _draw_single_box(frame_to_draw, box)
    elif 0 <= target_index < len(all_boxes):
        # 单目标模式：只绘制选中的那个框
        box_to_draw = all_boxes[target_index]
        _draw_single_box(frame_to_draw, box_to_draw)

    return frame_to_draw