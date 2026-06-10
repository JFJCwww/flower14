# Flowers14 - 基于 YOLOv8 的 14 种花朵分类

使用 YOLOv8 分类模型对 14 种花卉进行自动识别分类。

## 花卉类别

| 编号 | 英文名 | 中文名 |
|------|--------|--------|
| 0 | astilbe | 落新妇 |
| 1 | bellflower | 风铃草 |
| 2 | black_eyed_susan | 黑眼菊 |
| 3 | calendula | 金盏花 |
| 4 | california_poppy | 金英花 |
| 5 | carnation | 康乃馨 |
| 6 | common_daisy | 雏菊 |
| 7 | coreopsis | 金鸡菊 |
| 8 | dandelion | 蒲公英 |
| 9 | iris | 鸢尾花 |
| 10 | rose | 玫瑰 |
| 11 | sunflower | 向日葵 |
| 12 | tulip | 郁金香 |
| 13 | water_lily | 睡莲 |

## 项目结构

```
shixun/
├── train_yolo.py          # 训练脚本
├── predict.py             # 命令行推理脚本
├── work.py                # PyQt5 可视化识别界面
├── prepare_data.py        # 数据集准备脚本
├── flowers14.yaml         # 数据集配置文件
├── flowers14_data/        # YOLO 分类格式数据集
│   ├── train/             # 训练集（约 13642 张）
│   │   ├── astilbe/
│   │   ├── bellflower/
│   │   └── ...
│   └── val/               # 验证集（约 98 张）
│       ├── astilbe/
│       ├── bellflower/
│       └── ...
└── runs/
    └── classify/
        └── flowers14_cls-5/
            └── weights/
                ├── best.pt    # 最佳模型
                └── last.pt    # 最后一轮模型
```

## 环境依赖

```
Python >= 3.8
PyTorch >= 2.0
ultralytics >= 8.4
PyQt5  （仅 work.py 需要）
```

安装依赖：

```bash
pip install ultralytics PyQt5
```

## 使用方法

### 1. 数据准备

从 ModelScope 下载 flowers14 数据集并转换为 YOLO 分类格式：

```bash
python prepare_data.py
```

数据来源：[ModelScope - flowers14](https://www.modelscope.cn/datasets/tany0699/flowers14)

### 2. 训练模型

```bash
python train_yolo.py
```

训练参数：

| 参数 | 值 | 说明 |
|------|------|------|
| 模型 | yolov8n-cls.pt | YOLOv8-nano 分类模型 |
| epochs | 50 | 最大训练轮数 |
| imgsz | 224 | 输入图片尺寸 |
| batch | 32 | 批次大小 |
| patience | 10 | 早停轮数 |
| optimizer | auto | 自动选择优化器 |
| lr0 | 0.001 | 初始学习率 |
| cos_lr | True | 余弦学习率衰减 |

训练结果：

- Top-1 准确率：**96.9%**
- Top-5 准确率：**100%**
- 实际训练 12 轮（早停触发，最佳在第 2 轮）

### 3. 命令行推理

```bash
# 单张图片
python predict.py test.jpg

# 多张图片
python predict.py img1.jpg img2.jpg

# 整个文件夹
python predict.py test_folder/
```

输出示例：

```
加载模型: runs/classify/flowers14_cls-5/weights/best.pt

共 3 张图片，开始预测:

  rose.jpg: 玫瑰 (rose) - 置信度 98.72%
  sunflower.jpg: 向日葵 (sunflower) - 置信度 95.31%
  tulip.jpg: 郁金香 (tulip) - 置信度 91.45%
```

### 4. 可视化界面

```bash
python work.py
```

功能：

- 点击「开始识别」选择包含花朵图片的文件夹
- 自动轮播图片，每张图实时显示识别结果（中文花名 + 置信度）
- 支持上一张 / 下一张手动翻页
- 支持暂停 / 继续播放

## 技术细节

- **模型架构**：YOLOv8n-cls（nano 版本，约 3M 参数）
- **训练设备**：NVIDIA RTX 3060 Laptop GPU
- **训练时长**：约 13 分钟（12 轮）
- **数据增强**：由 ultralytics 自动应用（随机翻转、色彩抖动等）
- **早停机制**：patience=10，验证集精度不再提升时自动停止
