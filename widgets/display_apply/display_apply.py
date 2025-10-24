import sys
import csv
from pathlib import Path
from PySide6.QtWidgets import QApplication, QWidget, QSizePolicy, QTableWidgetItem, QFileDialog, QMessageBox, QHeaderView
from PySide6.QtGui import QFont,QMouseEvent
from PySide6.QtCore import QTimer, Qt,QPoint
from functions.yolo_api import YoloAPI, Box, FrameResult
from functions.media_handler import MediaHandler
from functions.camera_yolo_api import CameraYoloAPI
from functions.draw_yolo import draw_boxes
from functions.file_cp_selector import open_selector
from Ui_display import Ui_Form
import cv2
import numpy as np
from typing import Optional
from functions.title_bar_dragger import TitleBarDragger

project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from config import MODEL_STORE_PATH, INPUT_FILE_PATH,PLAY_INTERVAL_MS

class DisplayApp(QWidget):
    SHOULD_HIDE_TITLE_BAR: bool = True
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        if self.SHOULD_HIDE_TITLE_BAR:
            self.setWindowFlag(Qt.FramelessWindowHint)
            self._title_bar_dragger = TitleBarDragger(self, self.ui.lb_title)
            #self._title_bar_dragger.enable_drag()

        self.media_manager = MediaHandler(self.ui.display)
        self.playback_timer = QTimer(self)
        self.playback_timer.timeout.connect(self._process_and_display_frame)

        self.yolo: Optional[YoloAPI] = None
        YoloAPI.set_global_logging(True)

        self.camera_api: Optional[CameraYoloAPI] = None

        self.current_media_path: str = "N/A"
        self.all_detection_results: list[list] = []
        self.last_yolo_result: Optional[FrameResult] = None
        self._setup_table_widget()

        model_store_dir = Path(MODEL_STORE_PATH)
        default_model_path = model_store_dir / "best.pt"
        self.ui.le_model_path.setText(str(default_model_path))
        self.load_model(default_model_path)

        # ✅ 新增：幻灯片（图片文件夹）播放间隔，单位毫秒。在此处设置您想要的值。
        self.slideshow_interval_ms: int = PLAY_INTERVAL_MS

        self.bind()

        self.ui.lb_cameracheck.setText("摄像头: <font color='gray'>已关闭</font>")



    def bind(self):
        self.ui.btn_model_select.clicked.connect(self.select_and_load_model)
        self.ui.btn_open_one_file.clicked.connect(lambda: self.select_and_load_media('file'))
        self.ui.btn_open_dir.clicked.connect(lambda: self.select_and_load_media('dir'))
        self.ui.le_model_path.returnPressed.connect(self.on_model_path_entered)
        self.ui.le_open_one_file.returnPressed.connect(self.on_media_path_entered)
        self.ui.btn_camera.clicked.connect(self.toggle_camera)
        self.ui.cb_select_target.currentIndexChanged.connect(self.on_target_selection_change)
        self.ui.btn_exit.clicked.connect(self.close)
        self.ui.btn_save.clicked.connect(self.save_results_to_csv)
        if hasattr(self.ui, 'btn_clear'):
            self.ui.btn_clear.clicked.connect(self._reset_session_with_confirmation)

    def select_and_load_model(self):
        path_str = open_selector(
            parent_widget=self,
            target_folder=MODEL_STORE_PATH,
            file_or_dir='file',
            label_widget=self.ui.le_model_path
        )

        if path_str:
            self.load_model(Path(path_str))

    def select_and_load_media(self, file_or_dir: str):
        target_label_widget = None
        if file_or_dir == 'file':
            target_label_widget = self.ui.le_open_one_file
        elif file_or_dir == 'dir':
            # 请确保你的Ui_display.py中存在 self.ui.le_open_dir
            target_label_widget = self.ui.le_open_dir
        else:
            QMessageBox.warning(self, "参数错误", "无效的媒体类型选择。")
            return

        path_str = open_selector(
            parent_widget=self,
            target_folder=INPUT_FILE_PATH,
            file_or_dir=file_or_dir,
            label_widget=target_label_widget
        )

        if path_str:
            self.load_media(Path(path_str))

    def on_model_path_entered(self):
        path_str = self.ui.le_model_path.text().strip()
        if path_str:
            self.load_model(Path(path_str))

    def on_media_path_entered(self):
        path_str = self.ui.le_open_one_file.text().strip()
        if path_str:
            self.load_media(Path(path_str))

    def stop_all_media_sources(self):
        """统一停止所有正在播放的媒体和摄像头"""
        self.playback_timer.stop()
        self.media_manager.release()
        if self.camera_api and self.camera_api.is_active:
            self.camera_api.stop()
            self.ui.lb_cameracheck.setText("摄像头: <font color='gray'>已关闭</font>")

        self.current_media_path = "N/A"
        self.ui.display.setText("空闲")
        self.clear_target_details()
        self.ui.lb_num.setText("0")
        self.ui.lb_time.setText("0.0 ms")

    def load_media(self, path: Path):
        self.stop_all_media_sources() # 停止所有当前活动源

        if path.suffix.lower() in {".pt", ".pth"}:
            QMessageBox.warning(self, "操作错误", "这是一个模型文件，请在'模型路径'输入框中加载。")
            return

        self.current_media_path = path.name

        # ✅ 修改：将 slideshow_interval_ms 传递给 media_manager.load
        effective_interval = self.media_manager.load(
            str(path),
            user_interval_ms=self.slideshow_interval_ms # 传递给 MediaHandler
        )

        if effective_interval is not None:
            self._process_and_display_frame() # 显示第一帧
            if effective_interval > 0: # 如果有效间隔大于0，则启动定时器
                self.playback_timer.start(effective_interval)
            # 如果 effective_interval 为 0，表示单张图片，无需定时器
        else:
            QMessageBox.critical(self, "加载失败", f"无法加载指定的媒体文件或文件夹:\n{path}")
            self.stop_all_media_sources()

    def start_camera(self):
        self.stop_all_media_sources()

        if not self.yolo:
            QMessageBox.warning(self, "操作错误", "请先加载一个有效的YOLO模型！");
            return

        if self.camera_api is None or self.camera_api.yolo is not self.yolo:
            try:
                self.camera_api = CameraYoloAPI(yolo_api=self.yolo, source=0)
            except Exception as e:
                QMessageBox.critical(self, "摄像头初始化失败", f"无法创建摄像头API实例: {e}");
                self.ui.lb_cameracheck.setText("摄像头: <font color='red'>初始化失败</font>")
                self.stop_all_media_sources()
                return

        if self.camera_api.start():
            self.playback_timer.start(33) # 约30帧/秒
            self.ui.lb_cameracheck.setText("摄像头: <font color='green'>已开启</font>")
            self.current_media_path = "Camera Source 0"
        else:
            self.ui.lb_cameracheck.setText("摄像头: <font color='red'>开启失败</font>")
            QMessageBox.critical(self, "摄像头启动失败", "未能成功启动摄像头。")
            self.stop_all_media_sources()

    def stop_camera(self):
        if self.camera_api and self.camera_api.is_active:
            self.camera_api.stop()
        self.stop_all_media_sources()

    def load_model(self, model_path: Path):
        if self.all_detection_results:
            self._reset_session_with_confirmation()

        self.stop_all_media_sources()
        QApplication.processEvents()

        new_api_instance = YoloAPI.create_instance(model_path, device="cpu")
        if new_api_instance:
            self.yolo = new_api_instance
            print(f"已加载模型: {model_path.name}")
            self.ui.display.setText(f"模型 '{model_path.name}' 已加载完毕。\n请打开图片或视频进行检测。")
            self.last_yolo_result = None
            self.clear_target_details()
            self.ui.lb_num.setText("0")
            self.ui.lb_time.setText("0.0 ms")
        else:
            self.yolo = None
            QMessageBox.critical(self, "加载失败", f"模型加载失败:\n{model_path.name}\n请检查路径或模型文件是否损坏。")

    def _setup_table_widget(self):
        headers = ["序号", "文件路径", "类别", "置信度", "坐标位置"]
        self.ui.tableWidget.setColumnCount(len(headers))
        self.ui.tableWidget.setHorizontalHeaderLabels(headers)
        compact_font = QFont()
        compact_font.setPointSize(9)
        self.ui.tableWidget.setFont(compact_font)
        self.ui.tableWidget.verticalHeader().setDefaultSectionSize(22)
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.ui.tableWidget.horizontalHeader().setMinimumSectionSize(100)

    def _reset_session_with_confirmation(self):
        if not self.all_detection_results:
            return
        reply = QMessageBox.question(self, '确认操作', '确定要清空所有检测记录吗？\n此操作不可撤销。',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.all_detection_results.clear()
            self.ui.tableWidget.setRowCount(0)
            self.last_yolo_result = None
            self.clear_target_details()
            self.ui.lb_num.setText("0")
            self.ui.lb_time.setText("0.0 ms")
            print("所有检测记录已清空。")

    def _process_and_display_frame(self):
        """
        处理并显示下一帧。此函数根据当前激活的媒体源（摄像头或媒体文件）进行分发。
        """
        result: Optional[FrameResult] = None
        frame: Optional[np.ndarray] = None

        if self.camera_api and self.camera_api.is_active:
            # 摄像头模式
            result = self.camera_api.process_next_frame(mirror_flip=True)
            if result is None:
                print("摄像头信号丢失或结束...")
                self.stop_camera()
                return
            frame = result["raw_frame"]
        else:
            # 媒体文件（图片或视频）模式
            success, frame = self.media_manager.get_next_frame()
            if not success:
                self.stop_all_media_sources()
                self.ui.display.setText("播放结束")
                return

            if self.yolo:
                try:
                    result = next(self.yolo.infer(frame))
                except StopIteration:
                    result = {"raw_frame": frame, "boxes": [], "speed": {'preprocess': 0, 'inference': 0, 'postprocess': 0}}
                except Exception as e:
                    print(f"YOLO推理发生错误: {e}")
                    result = {"raw_frame": frame, "boxes": [], "speed": {'preprocess': 0, 'inference': 0, 'postprocess': 0}}
            else:
                cv2.putText(frame, "No Model Loaded", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                result = {"raw_frame": frame, "boxes": [], "speed": {'preprocess': 0, 'inference': 0, 'postprocess': 0}}

        if result:
            # 确保 media_manager 的 last_raw_frame 被更新，以供resizeEvent使用
            self.media_manager.last_raw_frame = result["raw_frame"] # 存储原始帧数据
            self.last_yolo_result = result
            self.update_ui_with_results(result)
        elif frame is not None:
            self.media_manager.last_raw_frame = frame # 存储原始帧数据
            self.media_manager.draw_frame(frame)
            self.last_yolo_result = {"raw_frame": frame, "boxes": [], "speed": {'preprocess': 0, 'inference': 0, 'postprocess': 0}}
            self.update_ui_with_results(self.last_yolo_result)


    def update_ui_with_results(self, result: FrameResult):
        speed = result["speed"]
        total_time = speed['preprocess'] + speed['inference'] + speed['postprocess']
        self.ui.lb_time.setText(f"{total_time:.1f} ms")

        boxes = result["boxes"]
        self.current_frame_boxes = boxes
        self.ui.lb_num.setText(str(len(boxes)))

        self.ui.cb_select_target.blockSignals(True)
        self.ui.cb_select_target.clear()
        if len(boxes) > 1:
            self.ui.cb_select_target.addItem("All")
            for i, box in enumerate(boxes):
                self.ui.cb_select_target.addItem(f"{box[6]} {i}", userData=i)
        elif len(boxes) == 1:
            self.ui.cb_select_target.addItem(f"{boxes[0][6]} 0", userData=0)
        else:
            self.ui.cb_select_target.addItem("None")
            self.clear_target_details()

        self.ui.cb_select_target.blockSignals(False)

        self.on_target_selection_change(self.ui.cb_select_target.currentIndex())

        self._add_detections_to_table(boxes)

    def on_target_selection_change(self, index: int):
        target_index_in_boxes = self.ui.cb_select_target.itemData(index)

        if target_index_in_boxes is None or not self.current_frame_boxes:
            self.clear_target_details()
        else:
            box = self.current_frame_boxes[target_index_in_boxes]
            confidence, cls_name = box[4], box[6]
            x1, y1, x2, y2 = box[0], box[1], box[2], box[3]

            self.ui.lb_conf.setText(f"{confidence:.2f}")
            self.ui.lb_type.setText(cls_name)
            self.ui.lb_xmin.setText(str(int(x1)))
            self.ui.lb_ymin.setText(str(int(y1)))
            self.ui.lb_xmax.setText(str(int(x2)))
            self.ui.lb_ymax.setText(str(int(y2)))

        if self.last_yolo_result and self.media_manager.last_raw_frame is not None:
            highlight_index = target_index_in_boxes if isinstance(target_index_in_boxes, int) else None
            refreshed_frame = draw_boxes(
                raw_frame=self.media_manager.last_raw_frame, # 使用缓存的原始帧
                all_boxes=self.last_yolo_result["boxes"],
                target_index=highlight_index
            )
            self.media_manager.draw_frame(refreshed_frame)

    def _add_detections_to_table(self, boxes: list[Box]):
        for box in boxes:
            index = len(self.all_detection_results) + 1
            path = self.current_media_path
            class_name = box[6]
            confidence = f"{box[4]:.2f}"
            coords = f"({int(box[0])}, {int(box[1])}, {int(box[2])}, {int(box[3])})"

            row_data = [index, path, class_name, confidence, coords]
            self.all_detection_results.append(row_data)

            row_position = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row_position)
            for col, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(row_position, col, item)
        self.ui.tableWidget.scrollToBottom()

    def save_results_to_csv(self):
        if not self.all_detection_results:
            QMessageBox.warning(self, "无数据", "没有检测结果可以保存。")
            return

        default_path = str(Path.home() / "detection_results.csv")
        file_path, _ = QFileDialog.getSaveFileName(self, "保存结果", default_path, "CSV 文件 (*.csv)")

        if not file_path:
            return

        try:
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                headers = [self.ui.tableWidget.horizontalHeaderItem(i).text()
                           for i in range(self.ui.tableWidget.columnCount())]
                writer.writerow(headers)
                writer.writerows(self.all_detection_results)
            QMessageBox.information(self, "保存成功", f"结果已成功保存到:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "保存失败", f"保存文件时发生错误:\n{e}")

    def clear_target_details(self):
        self.ui.lb_conf.setText("-")
        self.ui.lb_type.setText("-")
        self.ui.lb_xmin.setText("-")
        self.ui.lb_ymin.setText("-")
        self.ui.lb_xmax.setText("-")
        self.ui.lb_ymax.setText("-")

    def toggle_camera(self):
        if self.camera_api and self.camera_api.is_active:
            self.stop_camera()
        else:
            self.start_camera()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # ✅ 修改：确保 resizeEvent 使用 MediaHandler 缓存的最新原始帧，并重新绘制
        if self.last_yolo_result and self.media_manager.last_raw_frame is not None:
             # 重新绘制带有检测框的帧
            current_target_index = self.ui.cb_select_target.itemData(self.ui.cb_select_target.currentIndex())
            highlight_index = current_target_index if isinstance(current_target_index, int) else None

            # 使用 media_manager.last_raw_frame 作为 draw_boxes 的 raw_frame
            refreshed_frame = draw_boxes(
                raw_frame=self.media_manager.last_raw_frame,
                all_boxes=self.last_yolo_result["boxes"],
                target_index=highlight_index
            )
            self.media_manager.draw_frame(refreshed_frame)
        else:
            # 如果没有加载媒体或摄像头，清空显示
            self.ui.display.clear()
            self.ui.display.setText("空闲")


    def closeEvent(self, event):
        self.stop_all_media_sources()
        if self.yolo:
            del self.yolo
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DisplayApp()
    window.show()
    sys.exit(app.exec())