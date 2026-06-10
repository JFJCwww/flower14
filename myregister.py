import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QFormLayout,
    QHBoxLayout, QTextEdit
)
from PyQt5.QtCore import Qt


class Ui_Form:
    """UI 界面类，负责创建所有控件和布局"""
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        Form.setWindowTitle("注册窗口")

        # 创建控件
        self.labelName = QLabel(Form)
        self.labelName.setText("姓名：")

        self.lineEditName = QLineEdit(Form)
        self.lineEditName.setPlaceholderText("请输入姓名")

        self.labelPassword = QLabel(Form)
        self.labelPassword.setText("密码：")

        self.lineEditPassword = QLineEdit(Form)
        self.lineEditPassword.setEchoMode(QLineEdit.Password)
        self.lineEditPassword.setPlaceholderText("请输入密码")

        self.pushButton = QPushButton(Form)
        self.pushButton.setText("注册")

        # 新增的显示区域：用于展示用户名和密码，只读
        self.textDisplay = QTextEdit(Form)
        self.textDisplay.setReadOnly(True)
        self.textDisplay.setPlaceholderText("点击「注册」后，用户名和密码会显示在这里")
        # 设置固定最小高度，避免初始太小，但依然可以随窗口拉伸
        self.textDisplay.setMinimumHeight(100)

        # 表单单行布局（标签 + 输入框）
        formLayout = QFormLayout()
        formLayout.addRow(self.labelName, self.lineEditName)
        formLayout.addRow(self.labelPassword, self.lineEditPassword)

        # 按钮行布局（居中显示）
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.pushButton)
        buttonLayout.addStretch()

        # 主布局（垂直排列）
        mainLayout = QVBoxLayout(Form)
        mainLayout.addLayout(formLayout)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(self.textDisplay)  # 新增显示区域放在按钮下方

        # 设置边距和间距
        mainLayout.setContentsMargins(30, 30, 30, 30)
        mainLayout.setSpacing(20)

        # 可选：为关键控件设置对象名
        self.lineEditName.setObjectName("lineEditName")
        self.lineEditPassword.setObjectName("lineEditPassword")
        self.pushButton.setObjectName("pushButton")
        self.textDisplay.setObjectName("textDisplay")


class RegisterWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.register_btn)

    def register_btn(self):
        """注册按钮点击事件：获取输入内容并在原窗口的文本框中显示"""
        username = self.lineEditName.text().strip()
        password = self.lineEditPassword.text()

        # 构建显示信息
        display_text = f"您输入的用户名：{username}\n您输入的密码：{password}"
        # 显示到只读文本框中
        self.textDisplay.setText(display_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RegisterWindow()
    window.show()
    sys.exit(app.exec_())