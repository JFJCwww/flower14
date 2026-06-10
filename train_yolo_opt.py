# -*- coding: utf-8 -*-
"""
YOLOv8 花朵分类训练脚本 - 优化版
改进点:
  1. 更大模型: yolov8n-cls → yolov8s-cls
  2. 更大输入: 224 → 384
  3. 更多训练: 50 epochs → 100 epochs, patience 10 → 25
  4. 更强数据增强
  5. 学习率预热 + 余弦衰减
"""

from ultralytics import YOLO

if __name__ == '__main__':
    # 加载更大的预训练分类模型
    model = YOLO("yolov8s-cls.pt")

    # 开始训练
    results = model.train(
        data="D:/shixun/flowers14_data",  # 分类数据集目录
        epochs=100,                  # 训练轮数（增加到100）
        imgsz=384,                   # 输入图片尺寸（224→384，提升细节识别）
        batch=16,                    # 批次大小（imgsz增大，batch适当减小）
        name="flowers14_cls_v2",     # 实验名称
        patience=25,                 # 早停轮数（给更多收敛时间）
        device=0,                    # GPU 设备号
        workers=0,                   # Windows 下设为 0 避免多进程问题
        pretrained=True,             # 使用预训练权重
        optimizer="AdamW",           # AdamW 优化器
        lr0=0.001,                   # 初始学习率
        lrf=0.01,                    # 最终学习率 = lr0 * lrf
        cos_lr=True,                 # 余弦学习率衰减
        warmup_epochs=5,             # 学习率预热轮数

        # 数据增强
        hsv_h=0.015,                 # 色调抖动
        hsv_s=0.7,                   # 饱和度抖动
        hsv_v=0.4,                   # 亮度抖动
        translate=0.1,               # 平移
        scale=0.5,                   # 缩放
        fliplr=0.5,                  # 水平翻转
        erasing=0.4,                 # 随机擦除
        auto_augment="randaugment",  # 自动增强策略
    )

    print("\n" + "=" * 50)
    print("优化训练完成!")
    print(f"最佳模型: runs/classify/flowers14_cls_v2/weights/best.pt")
    print("=" * 50)
