# -*- coding: utf-8 -*-
import sys
import os
import warnings
from PyQt5 import QtCore, QtGui, QtWidgets
from ultralytics import YOLO

warnings.filterwarnings("ignore", category=DeprecationWarning)

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

# 全局样式表
STYLE_SHEET = """
QWidget {
    font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
    background-color: #f5f7fa;
}

/* 标题栏 */
QLabel#label_title {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #667eea, stop:1 #764ba2);
    color: white;
    font-size: 20px;
    font-weight: bold;
    padding: 14px;
    border-radius: 10px;
}

/* 图片显示区 */
QLabel#label_image {
    background-color: white;
    border: 2px solid #e0e6ed;
    border-radius: 12px;
    padding: 6px;
}

/* 识别结果卡片 */
QFrame#result_card {
    background-color: white;
    border-radius: 12px;
    border: 1px solid #e0e6ed;
}

QLabel#label_result_title {
    color: #667eea;
    font-size: 13px;
    font-weight: bold;
    padding: 0;
}

QLabel#label_result_flower {
    color: #2d3748;
    font-size: 26px;
    font-weight: bold;
    padding: 0;
}

QLabel#label_result_conf {
    color: #68d391;
    font-size: 18px;
    font-weight: bold;
    padding: 0;
}

/* 文件信息卡片 */
QFrame#file_card {
    background-color: white;
    border-radius: 12px;
    border: 1px solid #e0e6ed;
}

QLabel#label_file_title {
    color: #a0aec0;
    font-size: 12px;
    padding: 0;
}

QLabel#label_filename {
    color: #4a5568;
    font-size: 13px;
    padding: 0;
}

QLabel#label_progress {
    color: #a0aec0;
    font-size: 12px;
    padding: 0;
}

/* 按钮 */
QPushButton {
    font-size: 14px;
    font-weight: bold;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 20px;
}

QPushButton#btn_start {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #667eea, stop:1 #764ba2);
}

QPushButton#btn_start:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #5a6fd6, stop:1 #6a4192);
}

QPushButton#btn_start:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #4e60c2, stop:1 #5e3782);
}

QPushButton#btn_stop {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #fc8181, stop:1 #f687b3);
}

QPushButton#btn_stop:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #e06060, stop:1 #e07098);
}

QPushButton#btn_stop:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #c05050, stop:1 #c06080);
}

QPushButton#btn_prev, QPushButton#btn_next {
    background-color: #edf2f7;
    color: #4a5568;
    font-size: 18px;
    padding: 8px 16px;
    border: 1px solid #e2e8f0;
}

QPushButton#btn_prev:hover, QPushButton#btn_next:hover {
    background-color: #e2e8f0;
}

/* 进度条 */
QProgressBar {
    border: none;
    border-radius: 4px;
    background-color: #e2e8f0;
    height: 8px;
    text-align: center;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #667eea, stop:1 #764ba2);
    border-radius: 4px;
}

/* 底部信息 */
QLabel#label_footer {
    color: #a0aec0;
    font-size: 11px;
}
"""


class ImagePlayer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("Form")
        self.setMinimumSize(860, 620)
        self.resize(900, 650)
        self.setWindowTitle("花朵识别器")
        self.setStyleSheet(STYLE_SHEET)

        # 初始化变量
        self.image_list = []
        self.current_index = 0
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(2000)

        # 加载花朵分类模型
        self.model = None
        if os.path.exists(MODEL_PATH):
            self.model = YOLO(MODEL_PATH)
            print(f"模型加载成功: {MODEL_PATH}")
        else:
            print(f"模型文件不存在: {MODEL_PATH}，请先训练模型")

        self.setup_ui()

        # 信号连接
        self.btn_start.clicked.connect(self.start_play)
        self.btn_stop.clicked.connect(self.stop_play)
        self.btn_prev.clicked.connect(self.prev_image)
        self.btn_next.clicked.connect(self.next_image)
        self.timer.timeout.connect(self.auto_next)

        self.label_result_flower.setText("等待识别")
        self.label_result_conf.setText("--")
        self.label_filename.setText("请选择图片文件夹")
        self.label_progress.setText("0 / 0")

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(16, 12, 16, 12)
        main_layout.setSpacing(10)

        # === 标题 ===
        self.label_title = QtWidgets.QLabel("花朵识别器  Flower Classifier")
        self.label_title.setObjectName("label_title")
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.label_title)

        # === 中间区域：图片 + 右侧面板 ===
        mid_layout = QtWidgets.QHBoxLayout()
        mid_layout.setSpacing(12)

        # -- 左侧：图片显示 --
        self.label_image = QtWidgets.QLabel("点击「开始识别」选择图片文件夹")
        self.label_image.setObjectName("label_image")
        self.label_image.setAlignment(QtCore.Qt.AlignCenter)
        self.label_image.setMinimumSize(400, 350)
        self.label_image.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        mid_layout.addWidget(self.label_image, stretch=3)

        # -- 右侧面板 --
        right_layout = QtWidgets.QVBoxLayout()
        right_layout.setSpacing(10)
        right_layout.setContentsMargins(0, 0, 0, 0)

        # 识别结果卡片
        result_card = QtWidgets.QFrame()
        result_card.setObjectName("result_card")
        result_card.setFixedWidth(220)
        result_layout = QtWidgets.QVBoxLayout(result_card)
        result_layout.setContentsMargins(16, 14, 16, 14)
        result_layout.setSpacing(4)

        self.label_result_title = QtWidgets.QLabel("识别结果")
        self.label_result_title.setObjectName("label_result_title")
        self.label_result_title.setAlignment(QtCore.Qt.AlignCenter)
        result_layout.addWidget(self.label_result_title)

        self.label_result_flower = QtWidgets.QLabel("等待识别")
        self.label_result_flower.setObjectName("label_result_flower")
        self.label_result_flower.setAlignment(QtCore.Qt.AlignCenter)
        result_layout.addWidget(self.label_result_flower)

        self.label_result_conf = QtWidgets.QLabel("--")
        self.label_result_conf.setObjectName("label_result_conf")
        self.label_result_conf.setAlignment(QtCore.Qt.AlignCenter)
        result_layout.addWidget(self.label_result_conf)

        right_layout.addWidget(result_card)

        # 文件信息卡片
        file_card = QtWidgets.QFrame()
        file_card.setObjectName("file_card")
        file_card.setFixedWidth(220)
        file_layout = QtWidgets.QVBoxLayout(file_card)
        file_layout.setContentsMargins(16, 12, 16, 12)
        file_layout.setSpacing(4)

        self.label_file_title = QtWidgets.QLabel("当前文件")
        self.label_file_title.setObjectName("label_file_title")
        file_layout.addWidget(self.label_file_title)

        self.label_filename = QtWidgets.QLabel("请选择图片文件夹")
        self.label_filename.setObjectName("label_filename")
        self.label_filename.setWordWrap(True)
        file_layout.addWidget(self.label_filename)

        self.label_progress = QtWidgets.QLabel("0 / 0")
        self.label_progress.setObjectName("label_progress")
        self.label_progress.setAlignment(QtCore.Qt.AlignRight)
        file_layout.addWidget(self.label_progress)

        # 进度条
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setValue(0)
        file_layout.addWidget(self.progress_bar)

        right_layout.addWidget(file_card)
        right_layout.addStretch()

        mid_layout.addLayout(right_layout, stretch=1)
        main_layout.addLayout(mid_layout, stretch=1)

        # === 底部控制栏 ===
        ctrl_layout = QtWidgets.QHBoxLayout()
        ctrl_layout.setSpacing(10)

        self.btn_prev = QtWidgets.QPushButton("<")
        self.btn_prev.setObjectName("btn_prev")
        self.btn_prev.setFixedSize(44, 44)
        self.btn_prev.setEnabled(False)
        ctrl_layout.addWidget(self.btn_prev)

        self.btn_start = QtWidgets.QPushButton("开始识别")
        self.btn_start.setObjectName("btn_start")
        self.btn_start.setMinimumHeight(44)
        ctrl_layout.addWidget(self.btn_start)

        self.btn_stop = QtWidgets.QPushButton("暂停")
        self.btn_stop.setObjectName("btn_stop")
        self.btn_stop.setMinimumHeight(44)
        self.btn_stop.setEnabled(False)
        ctrl_layout.addWidget(self.btn_stop)

        self.btn_next = QtWidgets.QPushButton(">")
        self.btn_next.setObjectName("btn_next")
        self.btn_next.setFixedSize(44, 44)
        self.btn_next.setEnabled(False)
        ctrl_layout.addWidget(self.btn_next)

        main_layout.addLayout(ctrl_layout)

        # === 底部提示 ===
        self.label_footer = QtWidgets.QLabel("Powered by YOLOv8  |  14 类花朵分类")
        self.label_footer.setObjectName("label_footer")
        self.label_footer.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.label_footer)

    def start_play(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(
            self, "选择图片文件夹", "./"
        )
        if not folder_path:
            return

        self.image_list = []
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')):
                self.image_list.append(os.path.join(folder_path, filename))

        if not self.image_list:
            QtWidgets.QMessageBox.warning(self, "警告", "所选文件夹中没有找到图片文件！")
            return

        self.current_index = 0
        self.progress_bar.setMaximum(len(self.image_list))
        self.show_current_image()
        self.timer.start()

        self.btn_stop.setEnabled(True)
        self.btn_prev.setEnabled(True)
        self.btn_next.setEnabled(True)
        self.btn_start.setText("重新选择")

    def stop_play(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn_stop.setText("继续")
        else:
            self.timer.start()
            self.btn_stop.setText("暂停")

    def auto_next(self):
        if self.current_index < len(self.image_list) - 1:
            self.current_index += 1
            self.show_current_image()
        else:
            self.timer.stop()
            self.btn_stop.setText("继续")
            self.label_result_flower.setText("播放完毕")
            self.label_result_conf.setText("")

    def prev_image(self):
        if not self.image_list:
            return
        if self.timer.isActive():
            self.timer.stop()
            self.btn_stop.setText("继续")
        self.current_index = max(0, self.current_index - 1)
        self.show_current_image()

    def next_image(self):
        if not self.image_list:
            return
        if self.timer.isActive():
            self.timer.stop()
            self.btn_stop.setText("继续")
        self.current_index = min(len(self.image_list) - 1, self.current_index + 1)
        self.show_current_image()

    def predict_flower(self, image_path):
        if self.model is None:
            return "模型未加载", ""
        try:
            results = self.model(image_path, verbose=False)
            r = results[0]
            cls_id = int(r.probs.top1)
            cls_name = r.names[cls_id]
            confidence = r.probs.top1conf.item()
            cn_name = FLOWER_CN.get(cls_name, cls_name)
            return cn_name, f"{confidence:.1%}"
        except Exception as e:
            return "识别失败", str(e)

    def show_current_image(self):
        image_path = self.image_list[self.current_index]

        pixmap = QtGui.QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(
            self.label_image.size(),
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        self.label_image.setPixmap(scaled_pixmap)

        self.label_filename.setText(os.path.basename(image_path))
        self.label_progress.setText(f"{self.current_index + 1} / {len(self.image_list)}")
        self.progress_bar.setValue(self.current_index + 1)

        flower_name, confidence = self.predict_flower(image_path)
        self.label_result_flower.setText(flower_name)
        if confidence:
            self.label_result_conf.setText(confidence)
        else:
            self.label_result_conf.setText("--")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ImagePlayer()
    window.show()
    sys.exit(app.exec_())
