# -*- coding: utf-8 -*-
"""
花朵分类推理脚本 - 14 种花
用法:
  python predict.py image.jpg              # 单张图片
  python predict.py img1.jpg img2.jpg      # 多张图片
  python predict.py test_folder/           # 整个文件夹
"""

import sys
import os
from ultralytics import YOLO

# 14 种花的中英文映射
FLOWER_CN = {
    "astilbe": "落新妇",
    "bellflower": "风铃草",
    "black_eyed_susan": "黑眼菊",
    "calendula": "金盏花",
    "california_poppy": "金英花",
    "carnation": "康乃馨",
    "common_daisy": "雏菊",
    "coreopsis": "金鸡菊",
    "dandelion": "蒲公英",
    "iris": "鸢尾花",
    "rose": "玫瑰",
    "sunflower": "向日葵",
    "tulip": "郁金香",
    "water_lily": "睡莲",
}

MODEL_PATH = "runs/classify/flowers14_cls-5/weights/best.pt"


def predict(model, img_path):
    """对单张图片进行预测"""
    results = model(img_path, verbose=False)
    r = results[0]
    cls_id = int(r.probs.top1)
    cls_name = r.names[cls_id]
    confidence = r.probs.top1conf.item()
    cn_name = FLOWER_CN.get(cls_name, cls_name)

    print(f"  {os.path.basename(img_path)}: {cn_name} ({cls_name}) - 置信度 {confidence:.2%}")
    return cls_name, confidence


def main():
    if len(sys.argv) < 2:
        print("用法: python predict.py <图片路径或文件夹>")
        print("示例:")
        print("  python predict.py test.jpg")
        print("  python predict.py test_folder/")
        sys.exit(1)

    # 加载模型
    if not os.path.exists(MODEL_PATH):
        print(f"模型文件不存在: {MODEL_PATH}")
        print("请先运行训练: python train_yolo.py")
        sys.exit(1)

    print(f"加载模型: {MODEL_PATH}")
    model = YOLO(MODEL_PATH)

    # 收集所有图片
    targets = sys.argv[1:]
    image_files = []
    for t in targets:
        if os.path.isdir(t):
            for f in os.listdir(t):
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp')):
                    image_files.append(os.path.join(t, f))
        elif os.path.isfile(t):
            image_files.append(t)
        else:
            print(f"跳过: {t} (不存在)")

    if not image_files:
        print("未找到任何图片文件")
        sys.exit(1)

    # 逐张预测
    print(f"\n共 {len(image_files)} 张图片，开始预测:\n")
    for img_path in image_files:
        try:
            predict(model, img_path)
        except Exception as e:
            print(f"  {os.path.basename(img_path)}: 预测失败 - {e}")


if __name__ == "__main__":
    main()
