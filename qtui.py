from PyQt5 import QtWidgets, QtCore
from untitled import Ui_Form
import time


class MyWindow(QtWidgets.QWidget, Ui_Form):
    _signal = QtCore.pyqtSignal(str)  # 定义信号,定义参数为str类型

    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.myButton.clicked.connect(self.myPrint)
        self._signal.connect(self.mySignal)  # 将信号连接到函数mySignal

    def myPrint(self):
        self.tb.setText("")
        self.tb.append("正在打印，请稍候")
        self._signal.emit("你妹，打印结束了吗，快回答！")

    def mySignal(self, string):
        print(string)
        self.tb.append("打印结束")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.show()
    sys.exit(app.exec_()) 