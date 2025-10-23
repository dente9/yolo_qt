# val.py

import torch
from ultralytics import YOLO
from functions.update_file import update_file
from pathlib import Path
from config import (  DATASET_YAML_PATH,MODEL_TO_VALIDATE,IMG_SIZE,BATCH_SIZE,VALIDATION_RUN_NAME,
    RUNS_DIR, ROOT_DIR,DEVICE_NAME,DEVICE
)

def main():
    """
    主验证函数。
    """
    print(f"检测到设备: {DEVICE_NAME}，将用于验证。")

    # 2. 检查配置文件中的路径是否存在
    if not MODEL_TO_VALIDATE.exists():
        print(f"[错误] 找不到要验证的模型权重文件: {MODEL_TO_VALIDATE}")
        print("请确保 config.py 中的 MODEL_TO_VALIDATE 路径是正确的。")
        print("您可能需要先运行 train.py 来生成 'best.pt' 文件。")
        return
    if not DATASET_YAML_PATH.exists():
        print(f"[错误] 找不到数据集配置文件: {DATASET_YAML_PATH}")
        return

    # 3. 加载模型并开始验证
    try:
        print(f"\n正在加载模型: {MODEL_TO_VALIDATE}")
        model = YOLO(MODEL_TO_VALIDATE)

        print(f"正在使用数据集 '{DATASET_YAML_PATH}' 进行验证...")
        metrics = model.val(
            data=str(DATASET_YAML_PATH),
            imgsz=IMG_SIZE,
            batch=BATCH_SIZE,
            device=DEVICE,
            project=str(RUNS_DIR),
            name=VALIDATION_RUN_NAME
        )

        print("\n" + "="*15 + " 验证结果摘要 " + "="*15)
        print(f"mAP50-95 (Box): {metrics.box.map:.4f}")
        print(f"   mAP50 (Box): {metrics.box.map50:.4f}")
        print(f"   mAP75 (Box): {metrics.box.map75:.4f}")
        print(f"验证结果的详细图表和数据保存在: {metrics.save_dir}")
        rel_val_dir  = Path(metrics.save_dir).relative_to(ROOT_DIR)
        update_file('config.py',{'VAL_INFO_DIR =': f'VAL_INFO_DIR = ROOT_DIR / "{rel_val_dir.as_posix()}"'})

        print("="*47)

    except Exception as e:
        print(f"验证过程中发生严重错误: {e}")


if __name__ == '__main__':
    main()