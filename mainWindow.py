# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(10, 10, 371, 61))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color:rgb(170, 170, 0)")
        self.label_6.setTextFormat(QtCore.Qt.AutoText)
        self.label_6.setScaledContents(False)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 760, 369, 219))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(12)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName("groupBox_4")
        self.information = QtWidgets.QTextEdit(self.groupBox_4)
        self.information.setGeometry(QtCore.QRect(3, 30, 361, 181))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.information.sizePolicy().hasHeightForWidth())
        self.information.setSizePolicy(sizePolicy)
        self.information.setTabletTracking(True)
        self.information.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.information.setAcceptDrops(False)
        self.information.setAutoFillBackground(True)
        self.information.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.information.setAutoFormatting(QtWidgets.QTextEdit.AutoAll)
        self.information.setTabChangesFocus(True)
        self.information.setReadOnly(True)
        self.information.setObjectName("information")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 80, 371, 81))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 170, 371, 71))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(390, 80, 1521, 951))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(False)
        self.progressBar.setGeometry(QtCore.QRect(10, 990, 371, 31))
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.automode = QtWidgets.QPushButton(self.centralwidget)
        self.automode.setGeometry(QtCore.QRect(10, 330, 271, 71))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.automode.setFont(font)
        self.automode.setCheckable(True)
        self.automode.setObjectName("automode")
        self.close = QtWidgets.QPushButton(self.centralwidget)
        self.close.setGeometry(QtCore.QRect(10, 410, 371, 71))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.close.setFont(font)
        self.close.setCheckable(False)
        self.close.setObjectName("close")
        self.loadsettings = QtWidgets.QPushButton(self.centralwidget)
        self.loadsettings.setGeometry(QtCore.QRect(10, 250, 371, 71))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.loadsettings.setFont(font)
        self.loadsettings.setObjectName("loadsettings")
        self.monPath = QtWidgets.QPushButton(self.centralwidget)
        self.monPath.setGeometry(QtCore.QRect(290, 330, 91, 71))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.monPath.setFont(font)
        self.monPath.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ic_brightness_low_black_24dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.monPath.setIcon(icon)
        self.monPath.setIconSize(QtCore.QSize(24, 24))
        self.monPath.setCheckable(False)
        self.monPath.setObjectName("monPath")
        self.circleYellow = QtWidgets.QPushButton(self.centralwidget)
        self.circleYellow.setGeometry(QtCore.QRect(1860, 10, 20, 20))
        self.circleYellow.setObjectName("circleYellow")
        self.circleRed = QtWidgets.QPushButton(self.centralwidget)
        self.circleRed.setGeometry(QtCore.QRect(1890, 10, 20, 20))
        self.circleRed.setObjectName("circleRed")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(390, 30, 71, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setVisible(0)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_6.setText(_translate("MainWindow", "Benano"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Detail"))
        self.pushButton.setText(_translate("MainWindow", "Load xyz file"))
        self.pushButton_3.setText(_translate("MainWindow", "Multiple Position Registration"))
        self.automode.setText(_translate("MainWindow", "Auto Mode"))
        self.close.setText(_translate("MainWindow", "Close"))
        self.loadsettings.setText(_translate("MainWindow", "Load Registration Settings"))
        self.circleYellow.setText(_translate("MainWindow", "PushButton"))
        self.circleRed.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_2.setText(_translate("MainWindow", "RGB"))