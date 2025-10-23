
# YoloAPI - 简洁强大的YOLO推理接口

`YoloAPI` 是一个轻量级、高性能的Python库，它将复杂的YOLO目标检测模型封装成一个极其简单易用的接口。无论您需要处理单张图片、整个图片文件夹、视频文件还是实时摄像头流，都可以通过同一个 `infer`方法轻松完成。

该API专为集成而设计，非常适合在桌面应用程序（如Qt、PySide）、后端服务或自动化脚本中使用。

## 特性**统一接口**: 使用单个 `infer()`方法处理所有类型的输入源。

- **智能源识别**: 自动区分图片、视频、文件夹和摄像头。
- **高效流式处理**: 采用Python生成器（`yield`）处理视频和摄像头流，内存占用极低。
- **高度可配置**: 轻松调整置信度、IOU阈值等推理参数。
- **全局日志控制**: 通过一个简单的全局开关，即可控制所有推理过程的详细日志输出，便于调试。
- **健壮稳定**: 内置完善的资源管理和错误处理机制。

## 安装与准备

1. **环境要求**:

   * Python 3.8+
   * PyTorch
   * OpenCV (`opencv-python`)
   * Ultralytics YOLO (`ultralytics`)
2. **安装依赖**:

   ```bash
   pip install torch opencv-python ultralytics
   ```
3. **项目结构**:
   请确保您的项目文件结构如下。`yolo_api.py`是核心API文件，`best.pt`是您的YOLO模型权重。

   ```
   your_project/
   ├── yolo_api.py
   └── best.pt
   ```

## 快速上手

在您的Python脚本中，首先导入并初始化 `YoloAPI`。

```python
from yolo_api import YoloAPI

# 初始化API
# 如果有GPU，可以指定 device="cuda"
api = YoloAPI(weight="best.pt", device="cpu")

# (可选) 全局开启详细的推理日志，便于调试
YoloAPI.set_global_logging(True)
```

## API 使用指南

`YoloAPI`的核心是 `infer`方法。它返回一个**生成器**，您可以通过 `for`循环来遍历处理结果。

每一帧的处理结果 `result`是一个字典，格式如下：

```python
{
    "frame": <numpy.ndarray>,  # 带有检测框和标签的BGR图像
    "boxes": [  # 检测到的所有物体的列表
        [x1, y1, x2, y2, confidence, class_id],
        ...
    ]
}
```

---

### 1. 推理单张图片

提供图片的完整路径。`infer`会处理这张图片并 `yield`一次结果。

```python
import cv2
from yolo_api import YoloAPI

api = YoloAPI()
image_path = "path/to/your/image.jpg"

for result in api.infer(image_path):
    # result 是包含 "frame" 和 "boxes" 的字典
    print("检测到的物体数量:", len(result["boxes"]))
    print("详细信息:", result["boxes"])

    # 显示结果
    cv2.imshow("Single Image Inference", result["frame"])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
```

### 2. 推理图片文件夹 (多图片)

提供包含多张图片的文件夹路径。`infer`会遍历文件夹中所有支持的图片（`.jpg`, `.png`等），并为每一张图片 `yield`一次结果。

```python
import cv2
from yolo_api import YoloAPI

api = YoloAPI()
folder_path = "path/to/your/image_folder/"

print(f"正在处理文件夹: {folder_path}")
for i, result in enumerate(api.infer(folder_path)):
    print(f"--- 图片 {i+1} ---")
    print("检测到的物体数量:", len(result["boxes"]))

    # 显示每一张结果
    cv2.imshow(f"Image Folder - Result {i+1}", result["frame"])

    # 按任意键处理下一张，按ESC退出
    if cv2.waitKey(0) & 0xFF == 27:
        break

cv2.destroyAllWindows()
```

### 3. 推理视频文件

提供视频文件的完整路径。`infer`会逐帧处理视频，并为每一帧 `yield`一次结果，直到视频结束。

```python
import cv2
from yolo_api import YoloAPI

api = YoloAPI()
video_path = "path/to/your/video.mp4"

# for循环会自动处理视频的读取和释放
for result in api.infer(video_path):
    # 显示实时推理结果
    cv2.imshow("Video Inference", result["frame"])

    # 按ESC键退出播放
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
```

### 4. 推理实时摄像头

提供摄像头的ID（通常 `0`代表默认摄像头）。`infer`会持续从摄像头捕获画面并进行推理，为每一帧 `yield`一次结果。

为了获得类似镜子的体验，推荐在调用时设置 `mirror_flip=True`。

```python
import cv2
from yolo_api import YoloAPI

api = YoloAPI()
camera_id = 0

print("正在打开摄像头... 按ESC键退出。")
for result in api.infer(camera_id, mirror_flip=True):
    # 显示实时摄像头推理结果
    cv2.imshow("Live Camera Inference", result["frame"])

    # 按ESC键退出
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
```

---

## 高级用法

`infer`方法支持多个可选参数来微调推理过程：

```python
api.infer(
    source,              # 数据源
    conf=0.25,           # 置信度阈值 (0.0 - 1.0)
    iou=0.45,            # IOU阈值，用于非极大值抑制 (0.0 - 1.0)
    mirror_flip=False    # 仅对摄像头/视频有效，是否进行水平翻转
)
```

**示例：使用较低的置信度阈值**

```python
# 这会检测到更多可能的目标，即使模型对它们的把握不大
for result in api.infer(camera_id, conf=0.1):
    # ...
```
