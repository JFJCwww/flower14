# -*- coding: utf-8 -*-
"""
YOLOv8 花朵分类训练脚本 - 14 种花
"""

from ultralytics import YOLO

if __name__ == '__main__':
    # 加载预训练的分类模型
    model = YOLO("yolov8n-cls.pt")

    # 开始训练
    results = model.train(
        data="D:/shixun/flowers14_data",  # 分类数据集目录
        epochs=50,                   # 训练轮数
        imgsz=224,                   # 输入图片尺寸
        batch=32,                    # 批次大小
        name="flowers14_cls",        # 实验名称
        patience=10,                 # 早停轮数
        device=0,                    # GPU 设备号
        workers=0,                   # Windows 下设为 0 避免多进程问题
        pretrained=True,             # 使用预训练权重
        optimizer="auto",            # 自动选择优化器
        lr0=0.001,                   # 初始学习率
        cos_lr=True,                 # 余弦学习率衰减
    )

    print("训练完成!")
    print(f"最佳模型: runs/classify/flowers14_cls/weights/best.pt")
