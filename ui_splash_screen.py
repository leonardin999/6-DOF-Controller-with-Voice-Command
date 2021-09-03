# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/Leonard/AppData/Local/Temp/splash_screenZtdogT.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SplashScreen(object):
    def setupUi(self, SplashScreen):
        SplashScreen.setObjectName("SplashScreen")
        SplashScreen.resize(777, 536)
        self.centralwidget = QtWidgets.QWidget(SplashScreen)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dropShadowFrame = QtWidgets.QFrame(self.centralwidget)
        self.dropShadowFrame.setStyleSheet("QFrame {    \n"
"    background-color:  rgb(220, 220, 220);\n"
"    border-radius: 10px;\n"
"}")
        self.dropShadowFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dropShadowFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dropShadowFrame.setObjectName("dropShadowFrame")
        self.label_title = QtWidgets.QLabel(self.dropShadowFrame)
        self.label_title.setGeometry(QtCore.QRect(30, 190, 711, 111))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet("color:  rgb(52, 59, 72);")
        self.label_title.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_title.setObjectName("label_title")
        self.label_description = QtWidgets.QLabel(self.dropShadowFrame)
        self.label_description.setGeometry(QtCore.QRect(110, 320, 521, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_description.setFont(font)
        self.label_description.setStyleSheet("color: rgb(98, 114, 164);")
        self.label_description.setAlignment(QtCore.Qt.AlignCenter)
        self.label_description.setObjectName("label_description")
        self.progressBar = QtWidgets.QProgressBar(self.dropShadowFrame)
        self.progressBar.setGeometry(QtCore.QRect(20, 360, 721, 20))
        self.progressBar.setStyleSheet("QProgressBar {\n"
"    \n"
"    background-color: rgb(98, 114, 164);\n"
"    color: rgb(200, 200, 200);\n"
"    border-style: none;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"}\n"
"QProgressBar::chunk{\n"
"    border-radius: 5px;\n"
"    background-color: rgb(85, 170, 255)\n"
"}")
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label_credits = QtWidgets.QLabel(self.dropShadowFrame)
        self.label_credits.setGeometry(QtCore.QRect(420, 480, 321, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_credits.setFont(font)
        self.label_credits.setStyleSheet("\n"
"background-color: transparent;\n"
"color: rgb(0, 0, 0)")
        self.label_credits.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_credits.setObjectName("label_credits")
        self.label_credits_2 = QtWidgets.QLabel(self.dropShadowFrame)
        self.label_credits_2.setGeometry(QtCore.QRect(-40, 0, 261, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_credits_2.setFont(font)
        self.label_credits_2.setStyleSheet("\n"
"background-color: transparent;\n"
"color: rgb(0, 0, 0)")
        self.label_credits_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_credits_2.setObjectName("label_credits_2")
        self.label_sys = QtWidgets.QLabel(self.dropShadowFrame)
        self.label_sys.setGeometry(QtCore.QRect(10, 470, 55, 16))
        self.label_sys.setStyleSheet("color:rgb(0, 0, 0)")
        self.label_sys.setObjectName("label_sys")
        self.label_version = QtWidgets.QLabel(self.dropShadowFrame)
        self.label_version.setGeometry(QtCore.QRect(10, 490, 121, 16))
        self.label_version.setStyleSheet("color: rgb(0, 0, 0)")
        self.label_version.setObjectName("label_version")
        self.btn_load = QtWidgets.QPushButton(self.dropShadowFrame)
        self.btn_load.setGeometry(QtCore.QRect(260, 380, 241, 28))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_load.setFont(font)
        self.btn_load.setStyleSheet("background-color: transparent;\n"
"color: rgb(98, 114, 164);")
        self.btn_load.setObjectName("btn_load")
        self.label = QtWidgets.QLabel(self.dropShadowFrame)
        self.label.setGeometry(QtCore.QRect(-40, 30, 661, 141))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("logo.png"))
        self.label.setObjectName("label")
        self.label_credits_3 = QtWidgets.QLabel(self.dropShadowFrame)
        self.label_credits_3.setGeometry(QtCore.QRect(430, 450, 311, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_credits_3.setFont(font)
        self.label_credits_3.setStyleSheet("\n"
"background-color: transparent;\n"
"color: rgb(0, 0, 0)")
        self.label_credits_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_credits_3.setObjectName("label_credits_3")
        self.label_credits_4 = QtWidgets.QLabel(self.dropShadowFrame)
        self.label_credits_4.setGeometry(QtCore.QRect(430, 430, 311, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_credits_4.setFont(font)
        self.label_credits_4.setStyleSheet("\n"
"background-color: transparent;\n"
"color: rgb(0, 0, 0)")
        self.label_credits_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_credits_4.setObjectName("label_credits_4")
        self.label_credits_5 = QtWidgets.QLabel(self.dropShadowFrame)
        self.label_credits_5.setGeometry(QtCore.QRect(430, 410, 311, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_credits_5.setFont(font)
        self.label_credits_5.setStyleSheet("\n"
"background-color: transparent;\n"
"color: rgb(0, 0, 0)")
        self.label_credits_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_credits_5.setObjectName("label_credits_5")
        self.label_2 = QtWidgets.QLabel(self.dropShadowFrame)
        self.label_2.setGeometry(QtCore.QRect(660, 10, 101, 71))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("Facuty_logo.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.dropShadowFrame)
        SplashScreen.setCentralWidget(self.centralwidget)

        self.retranslateUi(SplashScreen)
        QtCore.QMetaObject.connectSlotsByName(SplashScreen)

    def retranslateUi(self, SplashScreen):
        _translate = QtCore.QCoreApplication.translate
        SplashScreen.setWindowTitle(_translate("SplashScreen", "MainWindow"))
        self.label_title.setText(_translate("SplashScreen", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:400;\">ỨNG DỤNG </span><span style=\" font-size:20pt;\">NHẬN DIỆN GIỌNG NÓI </span><span style=\" font-size:20pt; font-weight:400;\">TRONG </span></p><p align=\"center\"><span style=\" font-size:20pt; font-weight:400;\">ĐIỀU KHIỂN </span><span style=\" font-size:20pt;\">CÁNH TAY ROBOT 6 BẬC</span><span style=\" font-size:20pt; font-weight:400;\">. </span></p></body></html>"))
        self.label_description.setText(_translate("SplashScreen", "<strong>APP</strong> DESCRIPTION"))
        self.label_credits.setText(_translate("SplashScreen", "<html><head/><body><p><span style=\" font-size:8pt; font-weight:600;\">Created</span><span style=\" font-size:8pt;\">: Audio Intelligent Processing Team (</span><span style=\" font-size:8pt; font-weight:600;\">DRC Lab</span><span style=\" font-size:8pt;\">)</span></p></body></html>"))
        self.label_credits_2.setText(_translate("SplashScreen", "<html><head/><body><p><span style=\" font-size:8pt;\">Ver: 3.0:: Created on </span><span style=\" font-size:8pt; font-weight:600;\">july 15th,2021</span><span style=\" font-size:8pt;\">.</span></p></body></html>"))
        self.label_sys.setText(_translate("SplashScreen", "System: "))
        self.label_version.setText(_translate("SplashScreen", "Version of Sytem:"))
        self.btn_load.setText(_translate("SplashScreen", "Loading..."))
        self.label_credits_3.setText(_translate("SplashScreen", "<html><head/><body><p><span style=\" font-size:8pt; font-weight:600;\">Instructor:</span><span style=\" font-size:8pt;\"> Dr. Đặng Xuân Ba.</span></p></body></html>"))
        self.label_credits_4.setText(_translate("SplashScreen", "<html><head/><body><p><span style=\" font-size:8pt;\">Phạm Việt Hoàng.</span></p></body></html>"))
        self.label_credits_5.setText(_translate("SplashScreen", "<html><head/><body><p><span style=\" font-size:8pt; font-weight:600;\">Students</span><span style=\" font-size:8pt;\">: Phùng Hưng Bình.</span></p></body></html>"))

