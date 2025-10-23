# train.py

import torch
from ultralytics import YOLO
from pathlib import Path
from functions.update_file import update_file


from config import (DATASET_YAML_PATH, INITIAL_MODEL_WEIGHT,EPOCHS,IMG_SIZE,
    BATCH_SIZE, TRAIN_RUN_NAME, RUNS_DIR, ROOT_DIR,DEVICE,DEVICE_NAME
)

def main():
    print(f"检测到设备: {DEVICE_NAME}，将用于训练。")
    model = YOLO(INITIAL_MODEL_WEIGHT)
    print("\n开始训练...")
    print(f"  - 数据集: {DATASET_YAML_PATH}")
    print(f"  - 训练轮数: {EPOCHS}")
    print(f"  - 结果将保存在: {RUNS_DIR / 'detect' / TRAIN_RUN_NAME}")
    print("-" * 30)

    try:
        results = model.train(
            data=str(DATASET_YAML_PATH),
            epochs=EPOCHS,
            imgsz=IMG_SIZE,
            batch=BATCH_SIZE,
            device=DEVICE,
            project=str(RUNS_DIR),
            name=TRAIN_RUN_NAME
        )
    except Exception as e:
        print(f"训练过程中发生严重错误: {e}")
        return

    print("\n训练完成！")
    final_weights_path = Path(results.save_dir) / 'weights' / 'best.pt'
    rel_pt_path = final_weights_path.relative_to(ROOT_DIR)
    rel_train_info_dir  = Path(results.save_dir).relative_to(ROOT_DIR)
    print(f"训练结果已保存在: {results.save_dir}")
    print(f"最佳模型权重位于: {final_weights_path}")
    print(f"\n提示：请在 config.py 中检查 MODEL_TO_VALIDATE 的路径是否正确，")
    print("然后运行 val.py 来评估模型性能。")
    update_file('config.py',{'MODEL_TO_VALIDATE =': f'MODEL_TO_VALIDATE = ROOT_DIR / "{rel_pt_path.as_posix()}"'})
    update_file('config.py',{'TRAIN_INFO_DIR =': f'TRAIN_INFO_DIR = ROOT_DIR / "{rel_train_info_dir.as_posix()}"'})


if __name__ == '__main__':
    main()