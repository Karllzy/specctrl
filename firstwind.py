# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'try.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(746, 513)
        MainWindow.setMinimumSize(QtCore.QSize(100, 100))
        MainWindow.setMaximumSize(QtCore.QSize(1000000, 1000000))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 280, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(50, 90, 391, 101))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.doubleSpinBox_returns_min = QtWidgets.QDoubleSpinBox(self.widget)
        self.doubleSpinBox_returns_min.setObjectName("doubleSpinBox_returns_min")
        self.gridLayout.addWidget(self.doubleSpinBox_returns_min, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.doubleSpinBox_maxdrawdown_min = QtWidgets.QDoubleSpinBox(self.widget)
        self.doubleSpinBox_maxdrawdown_min.setObjectName("doubleSpinBox_maxdrawdown_min")
        self.gridLayout.addWidget(self.doubleSpinBox_maxdrawdown_min, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.doubleSpinBox_sharp_max = QtWidgets.QDoubleSpinBox(self.widget)
        self.doubleSpinBox_sharp_max.setObjectName("doubleSpinBox_sharp_max")
        self.gridLayout.addWidget(self.doubleSpinBox_sharp_max, 3, 1, 1, 1)
        self.doubleSpinBox_returns_max = QtWidgets.QDoubleSpinBox(self.widget)
        self.doubleSpinBox_returns_max.setObjectName("doubleSpinBox_returns_max")
        self.gridLayout.addWidget(self.doubleSpinBox_returns_max, 2, 1, 1, 1)
        self.doubleSpinBox_sharp_min = QtWidgets.QDoubleSpinBox(self.widget)
        self.doubleSpinBox_sharp_min.setObjectName("doubleSpinBox_sharp_min")
        self.gridLayout.addWidget(self.doubleSpinBox_sharp_min, 3, 0, 1, 1)
        self.doubleSpinBox_maxdrawdown_max = QtWidgets.QDoubleSpinBox(self.widget)
        self.doubleSpinBox_maxdrawdown_max.setObjectName("doubleSpinBox_maxdrawdown_max")
        self.gridLayout.addWidget(self.doubleSpinBox_maxdrawdown_max, 1, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.line = QtWidgets.QFrame(self.widget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        spacerItem1 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 746, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.slan = QtWidgets.QStatusBar(MainWindow)
        self.slan.setObjectName("slan")
        MainWindow.setStatusBar(self.slan)
        self.actionlianjie = QtWidgets.QAction(MainWindow)
        self.actionlianjie.setObjectName("actionlianjie")
        self.actiondisconnect = QtWidgets.QAction(MainWindow)
        self.actiondisconnect.setObjectName("actiondisconnect")
        self.actionnihao = QtWidgets.QAction(MainWindow)
        self.actionnihao.setObjectName("actionnihao")
        self.actionnishabi = QtWidgets.QAction(MainWindow)
        self.actionnishabi.setObjectName("actionnishabi")
        self.action1hao = QtWidgets.QAction(MainWindow)
        self.action1hao.setObjectName("action1hao")
        self.action2 = QtWidgets.QAction(MainWindow)
        self.action2.setObjectName("action2")
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        self.pushButton_2.clicked.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.label_3.setText(_translate("MainWindow", "收益"))
        self.label_4.setText(_translate("MainWindow", "最大回撤"))
        self.label_5.setText(_translate("MainWindow", "sharp比"))
        self.label_2.setText(_translate("MainWindow", "最大值"))
        self.label.setText(_translate("MainWindow", "最小值"))
        self.pushButton.setText(_translate("MainWindow", "开始"))
        self.menu.setTitle(_translate("MainWindow", "开始"))
        self.menu_2.setTitle(_translate("MainWindow", "文件"))
        self.actionlianjie.setText(_translate("MainWindow", "connect"))
        self.actiondisconnect.setText(_translate("MainWindow", "disconnect"))
        self.actionnihao.setText(_translate("MainWindow", "nihao "))
        self.actionnishabi.setText(_translate("MainWindow", "nishabi"))
        self.action1hao.setText(_translate("MainWindow", "1hao "))
        self.action2.setText(_translate("MainWindow", "2"))