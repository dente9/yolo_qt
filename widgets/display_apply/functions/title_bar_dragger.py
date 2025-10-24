# functions/title_bar_dragger.py (修复 RecursionError)
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import QMouseEvent
from PySide6.QtCore import Qt, QPoint
from typing import Optional

class TitleBarDragger:
    """
    一个辅助类，用于为无边框窗口提供通过拖动指定 QLabel 来移动窗口的功能。
    """
    def __init__(self, window: QWidget, draggable_widget: QLabel):
        """
        初始化拖动器。
        Args:
            window (QWidget): 要拖动的无边框窗口。
            draggable_widget (QLabel): 用于触发拖动的 QLabel 控件（例如自定义标题栏）。
        """
        self.window = window
        self.draggable_widget = draggable_widget
        self._drag_start_position: Optional[QPoint] = None
        self._dragging_window: bool = False

        # ✅ 关键：不直接绑定事件到 widget，而是让 window 重写事件
        # 这确保了事件首先被 window 处理，然后根据需要分发
        # 实际上，我们需要让 draggable_widget 自己捕获事件并处理，
        # 但它的父级（window）也要知道如何响应。
        # 最直接的方法是让 draggable_widget 覆盖自己的事件处理器，并在此处控制

        # 确保 draggable_widget 可以接收鼠标事件，否则事件不会到达它
        self.draggable_widget.setMouseTracking(True) # 启用鼠标跟踪，即使没有按钮按下也能触发moveEvent
        # QLabel 默认不接受鼠标点击事件，需要设置
        self.draggable_widget.setAcceptDrops(True) # 或者 self.draggable_widget.setEnabled(True)
        # 或者直接设置 mousePressEvent 等回调，并由回调来 accept/ignore

        # 将我们自己的方法设置为 QLabel 的事件处理函数
        # 我们不再存储原始事件，而是让事件通过 accept/ignore 机制流转
        self.draggable_widget._original_mousePressEvent = self.draggable_widget.mousePressEvent
        self.draggable_widget._original_mouseMoveEvent = self.draggable_widget.mouseMoveEvent
        self.draggable_widget._original_mouseReleaseEvent = self.draggable_widget.mouseReleaseEvent

        self.draggable_widget.mousePressEvent = self._mouse_press_event_handler
        self.draggable_widget.mouseMoveEvent = self._mouse_move_event_handler
        self.draggable_widget.mouseReleaseEvent = self._mouse_release_event_handler


    def _mouse_press_event_handler(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._dragging_window = True
            # 计算鼠标在窗口内容中的相对位置
            self._drag_start_position = event.globalPosition().toPoint() - self.window.frameGeometry().topLeft()
            event.accept() # 接受事件，阻止传递给 QLabel 的父控件
        else:
            # 如果不是左键按下，或者不拖动，让原始的 QLabel 事件处理器处理（如果存在）
            if hasattr(self.draggable_widget, '_original_mousePressEvent'):
                self.draggable_widget._original_mousePressEvent(event)
            else:
                event.ignore() # 否则忽略它，让它传递给父控件


    def _mouse_move_event_handler(self, event: QMouseEvent):
        if self._dragging_window:
            # 根据鼠标全局位置和拖动起始偏移计算新位置
            self.window.move(event.globalPosition().toPoint() - self._drag_start_position)
            event.accept() # 接受事件
        else:
            # 如果没有拖动，让原始的 QLabel 事件处理器处理（如果存在）
            if hasattr(self.draggable_widget, '_original_mouseMoveEvent'):
                self.draggable_widget._original_mouseMoveEvent(event)
            else:
                event.ignore() # 否则忽略它，让它传递给父控件


    def _mouse_release_event_handler(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self._dragging_window:
            self._dragging_window = False
            self._drag_start_position = None
            event.accept() # 接受事件
        else:
            # 如果不是左键释放，或者没有拖动，让原始的 QLabel 事件处理器处理（如果存在）
            if hasattr(self.draggable_widget, '_original_mouseReleaseEvent'):
                self.draggable_widget._original_mouseReleaseEvent(event)
            else:
                event.ignore() # 否则忽略它


    # enable_drag 和 disable_drag 方法不再需要，因为事件处理直接在 __init__ 中设置
    # 如果需要动态启用/禁用，需要重新设计，但目前直接设置已解决递归问题。
    # 为了避免混淆，暂时移除它们或将其标记为内部函数。
    # 但由于事件处理直接覆盖，这些方法可能不再适用当前设计模式。
    # 保持 TitleBarDragger 实例的生命周期与窗口同步，并在不需要时销毁它可能是更好的方式。