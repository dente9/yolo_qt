# functions/media_handler.py
import cv2
import os
import numpy as np
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
from pathlib import Path
from typing import Optional, Union

class MediaHandler:
    TYPE_NONE = 0
    TYPE_IMAGE = 1 # 单张图片文件
    TYPE_VIDEO = 2 # 视频文件
    TYPE_SLIDESHOW = 3 # 图片文件夹幻灯片

    def __init__(self, display_label: QLabel):
        if not isinstance(display_label, QLabel):
            raise TypeError("display_label 必须是一个 QLabel 实例。")
        self.display_label = display_label
        self._last_drawn_pixmap: Optional[QPixmap] = None # 用于resizeEvent重绘
        self._reset_state()

    def _reset_state(self):
        self.cap: Optional[cv2.VideoCapture] = None
        self.media_list: list[Path] = []
        self.current_media_index: int = -1
        self.media_type: int = self.TYPE_NONE
        self._last_drawn_frame_data: Optional[np.ndarray] = None # 存储最后绘制的原始帧数据，用于 draw_boxes 后的重绘

    def load(self, path_str: str, user_interval_ms: Optional[int] = None) -> int | None:
        """
        加载媒体源。现在可以处理包含非 ASCII 字符的路径。
        Args:
            path_str (str): 媒体文件或文件夹的路径。
            user_interval_ms (Optional[int]): 用户指定的播放间隔（毫秒），
                                                主要用于 TYPE_SLIDESHOW 模式。
        Returns:
            int | None: 如果成功加载并需要定时器驱动，返回建议的定时器间隔（毫秒）。
                        如果加载单个图片，返回 0（表示无需定时器，一次性显示）。
                        如果加载失败，返回 None。
        """
        self.release()

        path = Path(path_str)

        if not path.exists():
            self.display_label.setText(f"路径不存在: {path}")
            return None

        if path.is_file():
            ext = path.suffix.lower()
            if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']:
                self.media_type = self.TYPE_IMAGE
                self.media_list = [path] # 存储 Path 对象
                self.current_media_index = 0
                return 0 # 单张图片，无需定时器
            elif ext in ['.mp4', '.avi', '.mov', '.mkv']:
                self.cap = cv2.VideoCapture(str(path))
                if not self.cap.isOpened():
                    self.release()
                    self.display_label.setText("无法打开视频")
                    return None
                self.media_type = self.TYPE_VIDEO
                fps = self.cap.get(cv2.CAP_PROP_FPS)
                # 视频文件使用其固有帧率，user_interval_ms目前不用于覆盖视频帧率
                return int(1000 / fps) if fps > 0 else 33
            else:
                self.display_label.setText(f"不支持的文件类型:\n{path.name}")
                return None

        elif path.is_dir():
            supported_image_formats = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
            media_files = [p for p in sorted(path.iterdir()) if p.suffix.lower() in supported_image_formats]

            if media_files:
                self.media_type = self.TYPE_SLIDESHOW
                self.media_list = media_files # 存储 Path 对象列表
                self.current_media_index = -1 # 第一次 get_next_frame 会递增到 0
                # 使用 user_interval_ms 作为幻灯片播放间隔，如果未提供或无效则默认2000ms
                return user_interval_ms if user_interval_ms is not None and user_interval_ms > 0 else 2000
            else:
                self.display_label.setText(f"文件夹中未找到支持的图片文件:\n{path.name}")
                return None
        return None

    def get_next_frame(self) -> tuple[bool, np.ndarray | None]:
        if self.media_type == self.TYPE_IMAGE:
            # 单张图片，只读取一次
            if self.current_media_index == 0:
                self.current_media_index = -1 # 标记为已读取
                path_to_read = self.media_list[0]
                try:
                    img_array = np.fromfile(path_to_read, dtype=np.uint8)
                    frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                    return (frame is not None, frame)
                except Exception as e:
                    print(f"读取图片失败 '{path_to_read.name}': {e}")
                    return (False, None)
            return (False, None) # 已经读取过，不再提供帧

        elif self.media_type == self.TYPE_SLIDESHOW:
            self.current_media_index = (self.current_media_index + 1) % len(self.media_list) # 循环播放
            path_to_read = self.media_list[self.current_media_index]
            try:
                img_array = np.fromfile(path_to_read, dtype=np.uint8)
                frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                return (frame is not None, frame)
            except Exception as e:
                print(f"读取图片失败 '{path_to_read.name}': {e}")
                return (False, None)

        elif self.media_type == self.TYPE_VIDEO:
            if self.cap and self.cap.isOpened():
                return self.cap.read()
            return (False, None)

        return (False, None)

    def draw_frame(self, frame: np.ndarray):
        if not isinstance(frame, np.ndarray) or frame.size == 0: return
        self._last_drawn_frame_data = frame # 缓存原始帧数据
        self._last_drawn_pixmap = self._frame_to_pixmap(frame) # 缓存pixmap
        self._draw_scaled_pixmap()

    def release(self):
        if self.cap: self.cap.release()
        self._reset_state()
        self._last_drawn_pixmap = None
        self.display_label.clear()
        self._last_drawn_frame_data = None # 清除缓存的帧数据

    def handle_resize(self):
        self._draw_scaled_pixmap()

    def _draw_scaled_pixmap(self):
        if self._last_drawn_pixmap and not self._last_drawn_pixmap.isNull():
            scaled_pm = self._last_drawn_pixmap.scaled(
                self.display_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.display_label.setPixmap(scaled_pm)
        else:
            self.display_label.clear() # 如果没有可绘制的pixmap，则清空

    @staticmethod
    def _frame_to_pixmap(frame: np.ndarray) -> QPixmap | None:
        if frame.ndim == 3 and frame.shape[2] == 3:
            try:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                return QPixmap.fromImage(qt_image)
            except Exception as e:
                print(f"帧到 QPixmap 转换失败: {e}")
                return None
        return None

    # ✅ 修改：为 last_raw_frame 添加 setter 方法
    @property
    def last_raw_frame(self) -> Optional[np.ndarray]:
        """获取最后绘制的原始帧数据 (getter)。"""
        return self._last_drawn_frame_data

    @last_raw_frame.setter
    def last_raw_frame(self, frame: Optional[np.ndarray]):
        """设置最后绘制的原始帧数据 (setter)。"""
        self._last_drawn_frame_data = frame