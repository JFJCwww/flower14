# -*- coding: utf-8 -*-
"""
flowers14 数据集 → YOLOv8 分类格式
支持两种数据来源:
  1. ModelScope MsDataset (需要 modelscope SDK 兼容版本)
  2. 手动下载 zip 包后放到 flowers14/ 目录下
"""

import os
import csv
import zipfile
import json
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "flowers14")          # 原始数据集目录
OUT_DIR = os.path.join(BASE_DIR, "flowers14_data")      # YOLO 格式输出目录

CLASS_NAMES = [
    "carnation", "iris", "bellflower", "california_poppy",
    "rose", "astilbe", "tulip", "calendula",
    "dandelion", "coreopsis", "black_eyed_susan", "water_lily",
    "sunflower", "common_daisy",
]

CN_NAMES = [
    "康乃馨", "鸢尾花", "风铃草", "金英花",
    "玫瑰", "落新妇", "郁金香", "金盏花",
    "蒲公英", "金鸡菊", "黑眼菊", "睡莲",
    "向日葵", "雏菊",
]


def convert_from_zip():
    """从 flowers14/train.zip 和 val.zip 解压并重组为 YOLO 分类格式"""
    for split, zip_name in [("train", "train.zip"), ("val", "val.zip")]:
        zip_path = os.path.join(SRC_DIR, zip_name)
        if not os.path.exists(zip_path):
            print(f"  未找到 {zip_path}")
            return False

        print(f"  解压 {zip_name}...")
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(SRC_DIR)

    # 解压后检查目录结构
    train_dir = os.path.join(SRC_DIR, "train")
    if not os.path.exists(train_dir):
        print("  解压后未找到 train/ 目录")
        return False

    # 重命名为 YOLO 标准类名
    for split in ["train", "val"]:
        split_src = os.path.join(SRC_DIR, split)
        split_dst = os.path.join(OUT_DIR, split)
        if os.path.exists(split_src) and not os.path.exists(split_dst):
            os.makedirs(OUT_DIR, exist_ok=True)
            os.rename(split_src, split_dst)

    return True


def convert_from_csv_images():
    """从 CSV 文件中读取路径，配合已有的图片目录重组为 YOLO 格式"""
    # 检查图片是否已经在 flowers14/train/ 下
    train_dir = os.path.join(SRC_DIR, "train")
    if os.path.exists(train_dir) and os.listdir(train_dir):
        print("  发现 flowers14/train/ 目录已有图片，直接使用...")
        for split in ["train", "val"]:
            split_src = os.path.join(SRC_DIR, split)
            split_dst = os.path.join(OUT_DIR, split)
            if os.path.exists(split_src) and not os.path.exists(split_dst):
                os.makedirs(OUT_DIR, exist_ok=True)
                os.rename(split_src, split_dst)
        return True

    # 检查图片是否在当前目录的 train/ 下
    train_dir = os.path.join(BASE_DIR, "train")
    if os.path.exists(train_dir) and os.listdir(train_dir):
        print("  发现 train/ 目录已有图片，直接使用...")
        for split in ["train", "val"]:
            split_src = os.path.join(BASE_DIR, split)
            split_dst = os.path.join(OUT_DIR, split)
            if os.path.exists(split_src) and not os.path.exists(split_dst):
                os.makedirs(OUT_DIR, exist_ok=True)
                os.rename(split_src, split_dst)
        return True

    return False


def convert_from_modelscope():
    """使用 ModelScope SDK 下载并转换"""
    try:
        from modelscope.msdatasets import MsDataset
        from modelscope.utils.constant import DownloadMode
    except ImportError:
        print("  modelscope 未安装或版本不兼容")
        return False

    print("  正在从 ModelScope 加载数据集...")
    for split_name in ["train", "validation"]:
        print(f"  加载 {split_name} 集...")
        ds = MsDataset.load(
            "flowers14", namespace="tany0699",
            subset_name="default", split=split_name,
            download_mode=DownloadMode.FORCE_REDOWNLOAD,
        )
        split = "val" if split_name == "validation" else split_name
        print(f"  转换 {split} 集 ({len(ds)} 张图片)...")
        for i, item in enumerate(ds):
            img = item["image"]
            label = item["category"]
            cls_name = CLASS_NAMES[label]
            save_dir = os.path.join(OUT_DIR, split, cls_name)
            os.makedirs(save_dir, exist_ok=True)
            if isinstance(img, str):
                # 路径字符串，直接复制
                import shutil
                shutil.copy2(img, os.path.join(save_dir, f"{i:06d}.jpg"))
            else:
                # PIL Image
                img.save(os.path.join(save_dir, f"{i:06d}.jpg"))
            if (i + 1) % 2000 == 0:
                print(f"    {i+1}/{len(ds)} 已完成...")
        print(f"  {split} 集完成!")

    return True


def verify_dataset():
    """验证数据集"""
    print("\n验证数据集:")
    for split in ["train", "val"]:
        split_dir = os.path.join(OUT_DIR, split)
        if not os.path.exists(split_dir):
            print(f"  [{split}] 不存在!")
            continue
        total = 0
        for cls_name in CLASS_NAMES:
            cls_dir = os.path.join(split_dir, cls_name)
            if os.path.exists(cls_dir):
                count = len([f for f in os.listdir(cls_dir) if f.endswith(('.jpg', '.png', '.jpeg'))])
                total += count
            else:
                print(f"  [{split}/{cls_name}] 目录不存在!")
        print(f"  [{split}] 共 {total} 张图片")


def create_yaml():
    """创建 YOLO 数据集配置文件"""
    yaml_path = os.path.join(BASE_DIR, "flowers14.yaml")
    yaml_content = f"""# Flowers14 YOLOv8 Classification Dataset
path: {OUT_DIR.replace(chr(92), '/')}
train: train
val: val

names:
  0: carnation
  1: iris
  2: bellflower
  3: california_poppy
  4: rose
  5: astilbe
  6: tulip
  7: calendula
  8: dandelion
  9: coreopsis
  10: black_eyed_susan
  11: water_lily
  12: sunflower
  13: common_daisy

nc: 14
"""
    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write(yaml_content)
    print(f"\n配置文件: {yaml_path}")


if __name__ == "__main__":
    if os.path.exists(os.path.join(OUT_DIR, "train")):
        print("flowers14_data 已存在，跳过数据准备。")
    else:
        print("=" * 50)
        print("Flowers14 数据集准备工具")
        print("=" * 50)

        # 方式1: 从 zip 文件
        print("\n[方式1] 检查 zip 文件...")
        if convert_from_zip():
            print("zip 文件转换成功!")
        else:
            # 方式2: 从已有图片目录
            print("\n[方式2] 检查已有图片目录...")
            if convert_from_csv_images():
                print("图片目录转换成功!")
            else:
                # 方式3: 从 ModelScope SDK
                print("\n[方式3] 尝试 ModelScope SDK 下载...")
                if convert_from_modelscope():
                    print("ModelScope 下载转换成功!")
                else:
                    print("\n所有方式均失败!")
                    print("请手动操作:")
                    print("  1. 从 ModelScope 下载 train.zip 和 val.zip")
                    print("     网址: https://www.modelscope.cn/datasets/tany0699/flowers14")
                    print("  2. 将 zip 文件放到 flowers14/ 目录下")
                    print("  3. 重新运行本脚本")
                    exit(1)

    verify_dataset()
    create_yaml()
    print("\n数据集准备完成! 可以开始训练:")
    print("  python train_yolo.py")
