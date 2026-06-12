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
├── train_yolo.py          # 小型训练脚本（yolov8n-cls, 224px）
├── train_yolo_opt.py      # 大型训练脚本（yolov8s-cls, 384px, 更强增强）
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
        ├── flowers14_cls/
        │   └── weights/
        │       ├── best.pt    # 小型训练最佳模型
        │       └── last.pt
        └── flowers14_cls_v2/
            └── weights/
                ├── best.pt    # 大型训练最佳模型
                └── last.pt
```

## 环境依赖

```
Python >= 3.8
PyTorch >= 2.0
ultralytics >= 8.4
PyQt5        （仅 work.py 需要）
openpyxl     （仅 work.py 需要，Excel 导出）
matplotlib   （仅 work.py 需要，数据可视化）
```

安装依赖：

```bash
pip install ultralytics PyQt5 openpyxl matplotlib
```

## 使用方法

### 1. 数据准备

从 ModelScope 下载 flowers14 数据集并转换为 YOLO 分类格式：

```bash
python prepare_data.py
```

数据来源：[ModelScope - flowers14](https://www.modelscope.cn/datasets/tany0699/flowers14)

### 2. 训练模型

提供两种训练脚本，根据需求选择：

#### 小型训练（快速验证）

```bash
python train_yolo.py
```

| 参数 | 值 | 说明 |
|------|------|------|
| 模型 | yolov8n-cls.pt | YOLOv8-nano 分类模型（约 3M 参数） |
| epochs | 50 | 最大训练轮数 |
| imgsz | 224 | 输入图片尺寸 |
| batch | 32 | 批次大小 |
| patience | 10 | 早停轮数 |
| optimizer | auto | 自动选择优化器 |
| lr0 | 0.001 | 初始学习率 |
| cos_lr | True | 余弦学习率衰减 |

训练结果：Top-1 准确率 **96.9%**，Top-5 准确率 **100%**，实际训练 12 轮。

#### 大型训练（追求精度）

```bash
python train_yolo_opt.py
```

| 参数 | 值 | 说明 |
|------|------|------|
| 模型 | yolov8s-cls.pt | YOLOv8-small 分类模型（约 5M 参数） |
| epochs | 100 | 最大训练轮数 |
| imgsz | 384 | 输入图片尺寸（更大，识别更多细节） |
| batch | 16 | 批次大小（imgsz 增大，batch 减小） |
| patience | 25 | 早停轮数 |
| optimizer | AdamW | AdamW 优化器 |
| warmup_epochs | 5 | 学习率预热轮数 |
| 数据增强 | randaugment | 更强的自动增强策略 |

训练结果：

| 指标 | 值 |
|------|------|
| 实际训练轮数 | 47 轮（早停于第 22 轮后未再提升） |
| 训练总耗时 | 2.355 小时 |
| 训练设备 | NVIDIA A10 |
| Top-1 准确率 | **100%** |
| Top-5 准确率 | **100%** |
| 验证集评估 | 4/4 批次，0.8 秒完成 |
| 模型参数量 | 5,093,134 |
| 计算量 | 12.5 GFLOPs |
| 最佳模型 | `best.pt` |

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
- 右侧面板实时显示各类花朵识别统计（数量 / 平均置信度）
- **保存结果**：将识别记录导出为 Excel 文件，包含「识别记录」和「统计汇总」两个工作表
- **导入可视化**：导入已保存的 Excel 文件，以图表形式展示数据，支持 4 种图表：
  - 数量柱状图：各花朵识别次数
  - 占比饼图：各花朵识别比例
  - 置信度分布：各花朵平均置信度横向对比
  - 置信度折线：逐张图片置信度变化趋势
  - 底部附带数据明细表格

## 技术细节

### 小型训练

- **模型架构**：YOLOv8n-cls（nano 版本，约 3M 参数）
- **训练设备**：NVIDIA RTX 3060 Laptop GPU
- **训练时长**：约 13 分钟（12 轮）
- **数据增强**：由 ultralytics 自动应用（随机翻转、色彩抖动等）
- **早停机制**：patience=10，验证集精度不再提升时自动停止

### 大型训练

- **模型架构**：YOLOv8s-cls（small 版本，5,093,134 参数，12.5 GFLOPs）
- **训练设备**：NVIDIA A10
- **训练时长**：2.355 小时（47 轮，早停于第 22 轮后未再提升）
- **数据增强**：randaugment 自动增强策略
- **最终精度**：Top-1 准确率 100%，Top-5 准确率 100%
