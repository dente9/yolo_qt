#config.py
from pathlib import Path
import torch
ROOT_DIR = Path(__file__).parent
RUNS_DIR = ROOT_DIR / 'runs'
DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
DEVICE_NAME = torch.cuda.get_device_name(DEVICE) if DEVICE.type == 'cuda' else 'CPU'
#项目定义
PROGECT_NAME = 'my_project'
DATASET_YAML_PATH = ROOT_DIR / 'resource' / "datasets"/'data.yaml'
INITIAL_MODEL_WEIGHT = ROOT_DIR/"resource"/"yolo11n.pt"
TRAIN_RUN_NAME,VALIDATION_RUN_NAME = f'{PROGECT_NAME}_train',f'{PROGECT_NAME}_val'
# 训练超参数
EPOCHS = 1
IMG_SIZE = 640
BATCH_SIZE = 16
#训练后信息存放目录
MODEL_TO_VALIDATE = ROOT_DIR / "runs/my_project_train5/weights/best.pt"
TRAIN_INFO_DIR = ROOT_DIR / "runs/my_project_train5"
VAL_INFO_DIR = ROOT_DIR / "runs/my_project_val6"
