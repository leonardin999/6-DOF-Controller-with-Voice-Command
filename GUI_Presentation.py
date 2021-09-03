# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 19:52:33 2021

@author: Leonard
"""

import sys
import matplotlib
from matplotlib import cm
import serial.tools.list_ports
import serial
from module_function_GUI import *
from feature_extraction_GUI import *
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as ticker
from matplotlib.animation import FuncAnimation
import numpy as np
import sounddevice as sd
counter = 0

import platform
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot

from PyQt5.QtMultimedia import QAudioDeviceInfo,QAudio,QCameraInfo

input_audio_deviceInfos = QAudioDeviceInfo.availableDevices(QAudio.AudioInput)
from GUI_Function import *
from ui_splash_screen import Ui_SplashScreen

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_facecolor('#343b48')
        fig.suptitle('DR3 Controller Simulation Flatform',color='white',fontsize=15)
        plt.style.use("seaborn-notebook")
        
        self.axes = fig.gca(projection='3d')
        self.axes.set_facecolor('#343b48')
        self.axes.set_xlim(10,-45)
        self.axes.set_ylim(-35, 35)
        self.axes.set_zlim(-5, 35)

        self.axes.set_xlabel('X_axis',color='white',fontsize=10)
        self.axes.set_ylabel('Y_axis',color='white',fontsize=10)
        self.axes.set_zlabel('Z_axis',color='white',fontsize=10)
        self.axes.tick_params(axis='x', colors='white')
        self.axes.tick_params(axis='y', colors='white')
        self.axes.tick_params(axis='z', colors='white')
        super(MplCanvas, self).__init__(fig)
        fig.tight_layout()
        
class MplCanvas_camera(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_facecolor('#343b48')
        fig.tight_layout()
        fig.suptitle('Camera Zooming',color='white',fontsize=15)
        plt.style.use("seaborn-notebook")
        self.axes = fig.gca(projection='3d')
        self.axes.set_facecolor('#343b48')
        self.axes.set_xlim(0,-45)
        self.axes.set_ylim(-35,0)
        self.axes.set_zlim(0,10)
        self.axes.set_xlabel('X_axis',color='white',fontsize=10)
        self.axes.set_ylabel('Y_axis',color='white',fontsize=10)
        self.axes.set_zlabel('Z_axis',color='white',fontsize=10)
        self.axes.tick_params(axis='x', colors='white')
        self.axes.tick_params(axis='y', colors='white')
        self.axes.tick_params(axis='z', colors='white')
        super(MplCanvas_camera, self).__init__(fig)
        fig.tight_layout()
        
class MplCanvas_spectrogram(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_facecolor('#343b48')
        fig.suptitle('Spectrogram Diagram',color='white',fontsize=15)
        plt.style.use("seaborn-notebook")
        self.axes = fig.gca(projection='3d')
        self.axes.set_facecolor('#343b48')
        self.axes.tick_params(axis='x', colors='white')
        self.axes.tick_params(axis='y', colors='white')
        self.axes.tick_params(axis='z', colors='white')
        self.axes.set_xlabel('Time(s)-Domain',color='white',fontsize=8)
        self.axes.set_ylabel('Frequency(Hz)-Domain',color='white',fontsize=8)
        self.axes.set_zlabel('Amplitude(DB)',color='white',fontsize=8)
        super(MplCanvas_spectrogram, self).__init__(fig)
        fig.tight_layout()
        
class MplCanvas_record(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_facecolor('#343b48')
        fig.tight_layout()
        fig.suptitle('Raw Recording-audio File',color='white',fontsize=15)
        plt.style.use("seaborn-notebook")
        self.ax = fig.add_subplot(111)
        self.ax.grid(True)
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        super(MplCanvas_record, self).__init__(fig)
        fig.tight_layout()
        
class MplCanvas_mfcc(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_facecolor('#343b48')
        fig.tight_layout()
        fig.suptitle('Mel Frequency Cepstral Coefficients',color='white',fontsize=15)
        plt.style.use("seaborn-notebook")
        self.ax = fig.add_subplot(111)
        self.ax.grid(True)
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        super(MplCanvas_mfcc, self).__init__(fig)
        fig.tight_layout()
        
class MplCanvas_analysis(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_facecolor('#343b48')
        fig.tight_layout()
        plt.style.use("seaborn-notebook")
        self.axes = fig.add_subplot(111)
        self.axes.grid(True)
        self.axes.xaxis.set_ticklabels([])
        self.axes.tick_params(axis='y', colors='white')
        super(MplCanvas_analysis, self).__init__(fig)
        #fig.tight_layout()
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = uic.loadUi('main_1207.ui',self)
        self.ui.resize(1016, 820)
        self.setWindowIcon(QtGui.QIcon('robotics.png'))
        self.setWindowTitle('DR3 Controller')
        self.threadpool = QtCore.QThreadPool()
        self.threadpool_2 = QtCore.QThreadPool()
        self.threadpool_3 = QtCore.QThreadPool()
        self.threadpool_read = QtCore.QThreadPool()
        self.threadpool_mode = QtCore.QThreadPool()
        self.threadpool_audio = QtCore.QThreadPool()
        self.threadpool_pick  = QtCore.QThreadPool()
        self.threadpool_drop= QtCore.QThreadPool()
        self.threadpool_camera= QtCore.QThreadPool()
        self.threadpool_square= QtCore.QThreadPool()
        self.threadpool_circle= QtCore.QThreadPool()
        self.threadpool_triangle= QtCore.QThreadPool()
        
        self.stackedWidget.setCurrentWidget(self.ui.page)
        self.ui.btn_page_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_1))

        self.ui.btn_page_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))

        self.ui.btn_page_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page))
        
        self.Btn_Toggle.clicked.connect(lambda: UIFunctions.toggleMenu(self, 772, True))
        self.btn_analysis.clicked.connect(lambda: UIFunctions.toggleMenu_analysis(self, 772, True))
        
        self.Btn_Toggle_2.clicked.connect(lambda: UIFunctions.toggleMenu_setting(self, 280, True))
        self.btn_camera.clicked.connect(lambda: UIFunctions.setup_camera(self))
        self.devices_list= []
        for device in input_audio_deviceInfos:
            self.devices_list.append(device.deviceName())
        self.list_device.addItems(self.devices_list)
        self.engine = pyttsx3.init() # object creation
        self.rate = self.engine.getProperty('rate')   # getting details of current speaking rate
        self.engine.setProperty('rate', 150)     # setting up new voice rate
        self.voices = self.engine.getProperty('voices')
        self.volume = self.engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
        self.engine.setProperty('volume',1)    # setting up volume level  between 0 and 1
        self.ui.engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')
        name = []
        actual_name =[]
        for voice in self.ui.voices:
            name =np.append(name,voice.name)
        for data in name:
            config = data.split()
            actual_name = np.append(actual_name,config[1])
        self.lis_assistant.addItems(actual_name)
        
        
        self.canvas = MplCanvas(self, width=50, height=50, dpi=70)
        self.canvas_spec = MplCanvas_spectrogram(self, width=50, height=50, dpi=70)
        self.canvas_record = MplCanvas_record(self, width=11, height=4, dpi=70)
        self.canvas_mfcc = MplCanvas_mfcc(self, width=11, height=4, dpi=70)
        self.canvas_camera = MplCanvas_camera(self, width=50, height=50, dpi=70)
        self.canvas_data1 = MplCanvas_analysis(self, width=50, height=50, dpi=70)
        self.canvas_data2 = MplCanvas_analysis(self, width=50, height=50, dpi=70)
        self.ui.formLayout.addWidget(self.canvas)
        self.ui.formLayout_2.addWidget(self.canvas_spec)
        self.ui.formLayout_3.addWidget(self.canvas_mfcc)
        self.ui.formLayout_8.addWidget(self.canvas_record)
        self.ui.formLayout_4.addWidget(self.canvas_camera)
        self.ui.formLayout_10.addWidget(self.canvas_data2)
        self.ui.formLayout_12.addWidget(self.canvas_data1)
        self.groupBox_3.hide()
        self.groupBox_4.hide()
        self.groupBox_6.hide()
        self.reference_plot = None
        self.acess = False
        self.ser =  serial.Serial()
        self.ser_rasp = serial.Serial()
        
        UIFunctions.uiDefinitions(self)

        self.StoragePos1 = np.array([-40,25,-5])
        self.StoragePos2 = np.array([-35,25,-5])
        self.StoragePos3 = np.array([-30,25,-5])
        self.square_position   = np.array([0,0,0])
        self.cylinder_position = np.array([0,0,0])
        self.triangle_position = np.array([0,0,0])
        self.angle_square = 0
        self.angle_circle = 0
        self.angle_triangle = 0
        
        self.btnconnect_rasp.clicked.connect(lambda: UIFunctions.connect_rasp_clicked(self))
        self.btnconnect_rasp.clicked.connect(lambda: self.start_worker_1())
        self.btn_disconnect_rasp.clicked.connect(lambda: UIFunctions.disconnect_rasp_clicked(self))
        
        self.btnconnect_arduino.clicked.connect(lambda: UIFunctions.connect_arduino_clicked(self))
        
        self.btn_disconnect_arduino.clicked.connect(lambda: UIFunctions.disconnect_arduino_clicked(self))
        
        
        self.btnstart_simu.clicked.connect(lambda:UIFunctions.start_simulation(self))
        self.mode_check.stateChanged.connect(lambda: UIFunctions.simulation_check(self))
        
        self.set_up_assistant.clicked.connect(lambda: UIFunctions.set_up_voice(self))
        self.test_voice.clicked.connect(lambda: UIFunctions.test_voices(self))
        self.btn_record.clicked.connect(lambda: UIFunctions.ask_for_control(self))
        self.btn_up.clicked.connect(lambda: UIFunctions.forward_signal(self))
        self.btn_down.clicked.connect(lambda: UIFunctions.backward_signal(self))
        self.btn_right.clicked.connect(lambda: UIFunctions.right_signal(self))
        self.btn_left.clicked.connect(lambda: UIFunctions.left_signal(self)) 
        self.btn_z_down.clicked.connect(lambda: UIFunctions.down_signal(self)) 
        self.btn_z_up.clicked.connect(lambda: UIFunctions.up_signal(self))
        self.btn_pick.clicked.connect(lambda: self.pick_function())
        self.btn_drop.clicked.connect(lambda: self.drop_function())
        
        self.plus_yaw.clicked.connect(lambda:UIFunctions.yawUpMethod(self))
        self.minus_yaw.clicked.connect(lambda:UIFunctions.yawDownMethod(self))
        self.plus_pitch.clicked.connect(lambda:UIFunctions.pitchUpMethod(self))
        self.minus_pitch.clicked.connect(lambda:UIFunctions.pitchDownMethod(self))
        self.plus_roll.clicked.connect(lambda:UIFunctions.rollupMethod(self))
        self.minus_roll.clicked.connect(lambda:UIFunctions.rollDownMethod(self))
        self.btn_send_2.clicked.connect(lambda:UIFunctions.send_inverse(self))
        self.btn_send.clicked.connect(lambda:UIFunctions.send_home(self))
        
        self.time_respond.valueChanged.connect(lambda: UIFunctions.valuechange(self))
        self.Btn_Toggle_3.clicked.connect(lambda: self.open_introduction())
        self.btn_camera.clicked.connect(lambda: self.start_worker_camera())
        
        self.choose_store.currentTextChanged.connect(lambda: UIFunctions.sumary_store(self))
        self.btn_open_file.clicked.connect(lambda: UIFunctions.open_file(self))
        self.btn_plt.clicked.connect(lambda: UIFunctions.display_result(self))
        self.btn_plotBar.clicked.connect(lambda: UIFunctions.plot_bar_chart(self))
    def open_introduction(self):
        self.intro = introduction()
        self.intro.show()
        
    def keyPressEvent(self, event): # doesnt work when app is in background
        if event.key() == Qt.Key_R:
            UIFunctions.ask_for_control(self)
        if event.key() == Qt.Key_H:
            UIFunctions.send_home(self)
            
    def start_worker_1(self):
        worker = Worker(self.start_stream_data_rasp, )
        self.threadpool.start(worker)	
    def start_worker_2(self):
        worker2 = Worker(self.start_stream_data_arduino, )
        self.threadpool_2.start(worker2)	
    def start_worker_3(self):
        worker3 = Worker(self.start_stream_pick_up_object, )
        self.threadpool_3.start(worker3)	
    def start_worker_read(self):
        worker_read = Worker(self.read, )
        self.threadpool_read.start(worker_read)	
        
    def start_worker_mode(self):
        worker4 = Worker(self.Tranjactory_simulation_mode, )
        self.threadpool_mode.start(worker4)	
        self.active = True
    def stop_worker_mode(self):
        self.active = False
        time.sleep(0.3)
        
    def start_pick_up_square(self):
        workers = Worker(self.pick_up_square, )
        self.threadpool_square.start(workers)	
        self.active_s = True
    def stop_pick_up_square(self):
        self.active_s = False
        time.sleep(0.3)
    def start_pick_up_circle(self):
        workerc = Worker(self.pick_up_circle, )
        self.threadpool_circle.start(workerc)	
        self.active_c = True
    def stop_pick_up_circle(self):
        self.active_c = False
        time.sleep(0.3)
    def start_pick_up_triangle(self):
        workert = Worker(self.pick_up_triangle, )
        self.threadpool_triangle.start(workert)	
        self.active_t = True
    def stop_pick_up_triangle(self):
        self.active_t = False
        time.sleep(0.3)
    
    def start_worker_audio(self):
        worker5 = Worker(self.audio_information_start, )
        self.active_audio = True
        self.threadpool_audio.start(worker5)	
        
    def stop_worker_audio(self):
        self.active_audio = False
        time.sleep(0.2)
        
    def pick_function(self):
        worker6 = Worker(self.start_pick_function, )
        self.threadpool_pick.start(worker6)	
    def drop_function(self):
        worker7 = Worker(self.start_drop_function, )
        self.threadpool_drop.start(worker7)	
        
    def start_worker_camera(self):
        worker8 = Worker(self.shape_simulation, )
        self.threadpool_camera.start(worker8)	
        
    def shape_simulation(self):
        while self.ser_rasp.isOpen() and self.check_camera.isChecked():
            try:
                self.canvas_camera.axes.clear()
                self.canvas_camera.axes.set_xlim(0,-45)
                self.canvas_camera.axes.set_ylim(-35,0)
                self.canvas_camera.axes.set_zlim(5,5)
                self.canvas_camera.axes.set_xlabel('X_axis',color='white',fontsize=10)
                self.canvas_camera.axes.set_ylabel('Y_axis',color='white',fontsize=10)
                self.canvas_camera.axes.set_zlabel('Z_axis',color='white',fontsize=10)
                self.canvas_camera.axes.tick_params(axis='x', colors='white')
                self.canvas_camera.axes.tick_params(axis='y', colors='white')
                self.canvas_camera.axes.tick_params(axis='z', colors='white')
                if  self.square_position[0] < 9999 and self.square_position[1] < 9999:
                    self.canvas_camera.axes.scatter(self.square_position[0], self.square_position[1],
                                              self.square_position[2],s =7000,marker="s",color='Blue')
                    self.canvas_camera.axes.scatter(self.square_position[0],self.square_position[1],
                                                    self.square_position[2],s =100,marker="o",color='black')
                    label_1 = '  ({:.2f},{:.2f})' .format(self.square_position[0], self.square_position[1])
                    self.canvas_camera.axes.text(self.square_position[0]-3, self.square_position[1],
                                                 self.square_position[2],label_1,fontsize=15,color='k')
                if self.cylinder_position[0] < 9999 and self.cylinder_position[1] < 9999:
                    self.canvas_camera.axes.scatter(self.cylinder_position[0], self.cylinder_position[1],
                                                    self.cylinder_position[2],s =7000,marker="o",color='Green')
                    self.canvas_camera.axes.scatter(self.cylinder_position[0], self.cylinder_position[1],
                                                    self.cylinder_position[2],s =100,marker="o",color='black')
                    label_2 = '  ({:.2f},{:.2f})' .format(self.cylinder_position[0], self.cylinder_position[1])
                    self.canvas_camera.axes.text(self.cylinder_position[0]-3, self.cylinder_position[1],
                                                 self.cylinder_position[2],label_2,fontsize=15,color='k')
                if self.triangle_position[0] < 9999 and self.triangle_position[1] < 9999:
                    self.canvas_camera.axes.scatter(self.triangle_position[0], self.triangle_position[1],
                                              self.triangle_position[2],s =7000,  marker="^",color='Yellow')
                    self.canvas_camera.axes.scatter(self.triangle_position[0], self.triangle_position[1],
                                                    self.triangle_position[2],s =100,marker="o",color='black')
                    label_3 = '  ({:.2f},{:.2f})' .format(self.triangle_position[0], self.triangle_position[1])
                    self.canvas_camera.axes.text(self.triangle_position[0]-3, self.triangle_position[1],
                                                 self.triangle_position[2],label_3,fontsize=15,color='k')
                self.canvas_camera.draw()
            except:
                pass
    def start_stream_data_arduino(self):
        while  self.ser.isOpen() and self.mode_check.isChecked() == False:
            try:
                strdata = self.ser.readline().decode()
                time.sleep(0.1)
                self.theta = strdata.split()
                self.x,self.y,self.z = UIFunctions.forward_kinemtic_draw(self.theta)
                self.current_x.setText(str(round(self.x[6],3)))
                self.current_y.setText(str(round(self.y[6],3)))
                self.current_z.setText(str(round(self.z[6],3)))
                if len(self.theta) == 6:
                    self.valuethe1.setText(self.theta[0])
                    self.valuethe2.setText(self.theta[1])
                    self.valuethe3.setText(self.theta[2])
                    self.valuethe4.setText(self.theta[3])
                    self.valuethe5.setText(self.theta[4])
                    self.valuethe6.setText(self.theta[5])
            except:
                pass
            
    def read(self):
        while self.ser.isOpen():
            try:
                self.canvas.axes.clear()
                self.canvas.axes.set_xlim(10,-45)
                self.canvas.axes.set_ylim(-45, 35)
                self.canvas.axes.set_zlim(-5, 35)
                self.canvas.axes.set_xlabel('X_axis',color='white',fontsize=10)
                self.canvas.axes.set_ylabel('Y_axis',color='white',fontsize=10)
                self.canvas.axes.set_zlabel('Z_axis',color='white',fontsize=10)
                self.canvas.axes.tick_params(axis='x', colors='white')
                self.canvas.axes.tick_params(axis='y', colors='white')
                self.canvas.axes.tick_params(axis='z', colors='white')
                self.canvas.axes.scatter(self.StoragePos1[0], self.StoragePos1[1],self.StoragePos1[2],s=400, marker="s",color='Blue')
                self.canvas.axes.scatter(self.StoragePos2[0], self.StoragePos2[1],self.StoragePos2[2],s=400, marker="o",color='Green')
                self.canvas.axes.scatter(self.StoragePos3[0], self.StoragePos3[1],self.StoragePos3[2],s=400, marker="^",color='yellow')
                self.canvas.axes.text(self.StoragePos2[0], self.StoragePos2[1],self.StoragePos2[2]+3,'STORAGE',fontsize=12,color='black')
                self.canvas.axes.plot([0.0,self.x[0]],[0.0,self.y[0]],[-5.0,self.z[0]], linewidth=10)
                self.canvas.axes.plot([self.x[0],self.x[1]],[self.y[0],self.y[1]],[self.z[0],self.z[1]], linewidth=9)
                self.canvas.axes.plot([self.x[1],self.x[2]],[self.y[1],self.y[2]],[self.z[1],self.z[2]],linewidth=9)
                self.canvas.axes.plot([self.x[2],self.x[3]],[self.y[2],self.y[3]],[self.z[2],self.z[3]],linewidth=9)
                self.canvas.axes.plot([self.x[3],self.x[4]],[self.y[3],self.y[4]],[self.z[3],self.z[4]],linewidth=9)
                self.canvas.axes.plot([self.x[4],self.x[5]],[self.y[4],self.y[5]],[self.z[4],self.z[5]],linewidth=9,color='red')
                self.canvas.axes.plot([self.x[5],self.x[6]],[self.y[5],self.y[6]],[self.z[5],self.z[6]],linewidth=9)
    
                self.canvas.axes.scatter(0, 0, -5,color='k', marker="s",s=350)
                self.canvas.axes.scatter(self.x[0], self.y[0], self.z[0], marker="o", color='k',s=200)
                self.canvas.axes.scatter(self.x[1], self.y[1], self.z[1], marker="o", color='k',s=200)
                self.canvas.axes.scatter(self.x[2], self.y[2], self.z[2], marker="o", color='k',s=200)
                self.canvas.axes.scatter(self.x[3], self.y[3], self.z[3], marker="o", color='k',s=200)
                self.canvas.axes.scatter(self.x[4], self.y[4], self.z[4], marker="o", color='k',s=200)
                self.canvas.axes.scatter(self.x[5], self.y[5], self.z[5], marker="o", color='k',s=200)
                self.canvas.axes.scatter(self.x[6], self.y[6],self.z[6],s=150, marker="o",color='orange')
                if self.ser_rasp.isOpen():
                    if  self.square_position[0] < 9999 and self.square_position[1] < 9999:
                        self.canvas.axes.scatter(self.square_position[0], self.square_position[1],
                                                  self.square_position[2],s =300,marker="s",color='Blue')
                    if self.cylinder_position[0] < 9999 and self.cylinder_position[1] < 9999:
                        self.canvas.axes.scatter(self.cylinder_position[0], self.cylinder_position[1],
                                                  self.cylinder_position[2],s =300,  marker="o",color='Green')
                    if self.triangle_position[0] < 9999 and self.triangle_position[1] < 9999:
                        self.canvas.axes.scatter(self.triangle_position[0], self.triangle_position[1],
                                                  self.triangle_position[2],s =300,  marker="^",color='Yellow')
                self.canvas.draw()
            except:
                pass
            
    def start_stream_data_rasp(self):
        while self.ser_rasp.isOpen():
            try:
                  strdata1 = self.ser_rasp.readline().decode()
                  time.sleep(0.1)
                  position = strdata1.split(',')
                  if len(position) == 9:
                    self.square_position = np.array([float(position[0]),float(position[1]),5.0])
                    self.cylinder_position = np.array([float(position[2]),float(position[3]),5.0])
                    self.triangle_position = np.array([float(position[4]),float(position[5]),5.0])
                    self.angle_square = position[6]
                    self.angle_circle = position[7]
                    self.angle_triangle = position[8]
                    if self.block_name.currentText().strip() == 'hình vuông':
                        if self.square_position[0]>= 9999 or self.square_position[1]>= 9999:
                            self.rasp_xpos.setText("")
                            self.rasp_ypos.setText("")
                            self.rasp_zpos.setText("")
                        else:
                            self.rasp_xpos.setText(str(self.square_position[0]))
                            self.rasp_ypos.setText(str(self.square_position[1]))
                            self.rasp_zpos.setText(str(self.square_position[2]))
                            
                    elif self.block_name.currentText().strip() == 'hình tròn':
                        if self.cylinder_position[0]>= 9999 or self.cylinder_position[1]>= 9999:
                            self.rasp_xpos.setText("")
                            self.rasp_ypos.setText("")
                            self.rasp_zpos.setText("")
                        else:
                            self.rasp_xpos.setText(str(self.cylinder_position[0]))
                            self.rasp_ypos.setText(str(self.cylinder_position[1]))
                            self.rasp_zpos.setText(str(self.cylinder_position[2]))
                    elif self.block_name.currentText().strip() == 'tam giác':
                        if self.triangle_position[0]>= 9999 or self.triangle_position[1]>= 9999:
                            self.rasp_xpos.setText("")
                            self.rasp_ypos.setText("")
                            self.rasp_zpos.setText("")
                        else:
                            self.rasp_xpos.setText(str(self.triangle_position[0]))
                            self.rasp_ypos.setText(str(self.triangle_position[1]))
                            self.rasp_zpos.setText(str(self.triangle_position[2]))
            except :
                pass

   
    def start_stream_pick_up_object(self):
        try:
            time.sleep(0.3)
            if self.rasp_xpos.text()=="" and self.rasp_ypos.text()=="" and self.rasp_zpos.text()=="":
                label = self.block_name.currentText()
                if label == 'hình vuông':
                    say = 'square'
                elif label == 'hình tròn':
                    say = 'circle'
                elif label == 'tam giác':
                    say = 'triangle'
                self.engine.say("Sorry Sir There is No block of "+say+" in the field. Try another command instead?")
                self.engine.runAndWait()
                self.engine.stop()
            else:
                self.block_name.setEnabled(False)
                if self.block_name.currentText().strip() =='hình vuông':
                    xpos = round(float(self.rasp_xpos.text()),1)
                    ypos = round(float(self.rasp_ypos.text()),1)
                    zpos = round(float(self.rasp_zpos.text()),1)
                    roll = pitch = 0
                    yaw = 0
                    self.stop_worker_mode()
                    UIFunctions.send(self,xpos,ypos,zpos,yaw,pitch,roll)
                    self.start_worker_mode()
                    time.sleep(self.time_respond.value()+2)
                    self.stop_worker_mode()
                    yaw=0; pitch =0 ;roll = 0
                    UIFunctions.send(self,self.StoragePos1[0],self.StoragePos1[1],self.StoragePos1[2]+10,yaw,pitch,roll)
                    self.start_pick_up_square()
                    time.sleep(self.time_respond.value())
                    self.stop_pick_up_square()
                    yaw=0; pitch =0 ;roll = 0
                    UIFunctions.send(self,self.StoragePos1[0],self.StoragePos1[1],self.StoragePos1[2],yaw,pitch,roll)
                    self.start_pick_up_square()
                    time.sleep(self.time_respond.value())
                    self.stop_pick_up_square()
                    
                elif self.block_name.currentText().strip() == 'hình tròn':
                    xpos = round(float(self.rasp_xpos.text()),1)
                    ypos = round(float(self.rasp_ypos.text()),1)
                    zpos = round(float(self.rasp_zpos.text()),1)
                    yaw =35; pitch = 90; roll = 0
                    self.stop_worker_mode()
                    UIFunctions.send(self,xpos,ypos,zpos,yaw,pitch,roll)
                    self.start_worker_mode()
                    time.sleep(self.time_respond.value()+2)
                    self.stop_worker_mode()
                    yaw=0; pitch =0 ;roll = 0
                    UIFunctions.send(self,self.StoragePos2[0],self.StoragePos2[1],self.StoragePos2[2]+10,yaw,pitch,roll)
                    self.start_pick_up_circle()
                    time.sleep(self.time_respond.value())
                    self.stop_pick_up_circle()
                    yaw=0; pitch =0 ;roll = 0
                    UIFunctions.send(self,self.StoragePos2[0],self.StoragePos2[1],self.StoragePos2[2],yaw,pitch,roll)
                    self.start_pick_up_circle()
                    time.sleep(self.time_respond.value())
                    self.stop_pick_up_circle()
                elif self.block_name.currentText().strip() == 'tam giác':
                    
                    xpos = round(float(self.rasp_xpos.text()),1)
                    ypos = round(float(self.rasp_ypos.text()),1)
                    zpos = round(float(self.rasp_zpos.text()),1)
                    yaw =0; pitch =90
                    roll = self.angle_triangle
                    self.stop_worker_mode()
                    UIFunctions.send(self,xpos,ypos,zpos,yaw,pitch,roll)
                    self.start_worker_mode()
                    time.sleep(self.time_respond.value()+2)
                    self.stop_worker_mode()
                    yaw=0; pitch =0 ;roll = 0
                    UIFunctions.send(self,self.StoragePos3[0],self.StoragePos3[1],self.StoragePos3[2]+10,yaw,pitch,roll)
                    self.start_pick_up_triangle()
                    time.sleep(self.time_respond.value())
                    self.stop_pick_up_triangle()
                    yaw=0; pitch =0 ;roll = 0
                    UIFunctions.send(self,self.StoragePos3[0],self.StoragePos3[1],self.StoragePos3[2],yaw,pitch,roll)
                    self.start_pick_up_triangle()
                    time.sleep(self.time_respond.value())
                    self.stop_pick_up_triangle()
                time.sleep(0.1)
                x = -11.8
                y = 0.0
                z = 13.1
                yaw=0; pitch =0 ;roll = 0
                UIFunctions.send(self,x,y,z,yaw,pitch,roll)
                self.start_worker_mode()
                time.sleep(self.time_respond.value())
                self.block_name.setEnabled(True)
                self.engine.say("Product have been placed in the storage. Process succeed. Wake me up if you need anything")
                self.engine.runAndWait()
                self.engine.stop()
        except:
            x = -11.8
            y = 0.0
            z = 13.1
            yaw=0; pitch =0 ;roll = 0
            self.stop_pick_up_circle()
            self.stop_pick_up_square()
            self.stop_pick_up_triangle()
            self.stop_worker_mode()
            UIFunctions.send(self,x,y,z,yaw,pitch,roll)
            self.start_worker_mode()
            time.sleep(self.time_respond.value())
            self.block_name.setEnabled(True)
            self.engine.say("Error Alert. Try again on next time")
            self.engine.runAndWait()
            self.engine.stop()
        
    def Tranjactory_simulation_mode(self):
        self.idx=0
        while self.mode_check.isChecked() and self.idx <= self.time_respond.value()*10-30 and self.active == True:
            try:
                #self.timeqh = self.time_respond.value()*10
                tc = self.time_respond.value()
                x = float(self.xposvalue.text())
                y = float(self.yposvalue.text())
                z = float(self.zposvalue.text())
                yaw = float(self.yaw_value.text())
                pitch = float(self.pitch_value.text())
                roll = float(self.roll_value.text())
                the = np.round_(UIFunctions.inverse_kinematic(x,y,z,yaw,pitch,roll),5)
                a1 = self.the1pre
                b1 = 0
                c1 = 3 * (the[0]- self.the1pre) / tc ** 2
                d1 = -2 * (the[0] - self.the1pre) / tc ** 3
    
                a2 = self.the2pre
                b2 = 0
                c2 = 3 * (the[1]- self.the2pre) / tc ** 2
                d2 = -2 * (the[1]- self.the2pre) / tc ** 3
    
                a3 = self.the3pre
                b3 = 0
                c3 = 3 * (the[2] - self.the3pre) / tc ** 2
                d3 = -2 * (the[2] - self.the3pre) / tc ** 3
    
                a4 = self.the4pre
                b4 = 0
                c4 = 3 * (the[3] - self.the4pre) / tc ** 2
                d4 = -2 * (the[3] - self.the4pre) / tc ** 3
    
                a5 = self.the5pre
                b5 = 0
                c5 = 3 * (the[4] - self.the5pre) / tc ** 2
                d5 = -2 * (the[4] - self.the5pre) / tc ** 3
    
                a6 = self.the6pre
                b6 = 0
                c6 = 3 * (the[5]- self.the6pre) /tc ** 2
                d6 = -2 * (the[5] - self.the6pre) / tc ** 3
                self.label_time2.setText('Response Time:   '+str(float(self.idx/10))+'s')
                self.the1_flex = np.round(a1 + b1 * self.idx / 10 + c1 * (self.idx / 10) * 2 + d1 * (self.idx / 10) * 3, 4)
                self.the2_flex = np.round(a2 + b2 * self.idx / 10 + c2 * (self.idx / 10) * 2 + d2 * (self.idx / 10) * 3, 4)
                self.the3_flex = np.round(a3 + b3 * self.idx / 10 + c3 * (self.idx / 10) * 2 + d3 * (self.idx / 10) * 3, 4)
                self.the4_flex = np.round(a4 + b4 * self.idx / 10 + c4 * (self.idx / 10) * 2 + d4 * (self.idx / 10) * 3, 4)
                self.the5_flex = np.round(a5 + b5 * self.idx / 10 + c5 * (self.idx / 10) * 2 + d5 * (self.idx / 10) * 3, 4)
                self.the6_flex = np.round(a6 + b6 * self.idx / 10 + c6 * (self.idx / 10) * 2 + d6 * (self.idx / 10) * 3, 4)

                theta_flex = np.array([self.the1_flex,self.the2_flex,self.the3_flex,self.the4_flex,self.the5_flex,self.the6_flex])
                x,y,z = UIFunctions.forward_kinemtic_draw(theta_flex)
                self.current_x.setText(str(round(x[6],3)))
                self.current_y.setText(str(round(y[6],3)))
                self.current_z.setText(str(round(z[6],3)))
                self.canvas.axes.clear()
                self.canvas.axes.set_xlim(10,-45)
                self.canvas.axes.set_ylim(-45, 35)
                self.canvas.axes.set_zlim(-5, 35)
                self.canvas.axes.set_xlabel('X_axis',color='white',fontsize=10)
                self.canvas.axes.set_ylabel('Y_axis',color='white',fontsize=10)
                self.canvas.axes.set_zlabel('Z_axis',color='white',fontsize=10)
                self.canvas.axes.tick_params(axis='x', colors='white')
                self.canvas.axes.tick_params(axis='y', colors='white')
                self.canvas.axes.tick_params(axis='z', colors='white')
                if self.ser_rasp.isOpen():
                    if  self.square_position[0] < 9999 and self.square_position[1] < 9999:
                        self.canvas.axes.scatter(self.square_position[0], self.square_position[1],
                                                  self.square_position[2],s =300,marker="s",color='Blue')
                    if self.cylinder_position[0] < 9999 and self.cylinder_position[1] < 9999:
                        self.canvas.axes.scatter(self.cylinder_position[0], self.cylinder_position[1],
                                                  self.cylinder_position[2],s =300,  marker="o",color='Green')
                    if self.triangle_position[0] < 9999 and self.triangle_position[1] < 9999:
                        self.canvas.axes.scatter(self.triangle_position[0], self.triangle_position[1],
                                                  self.triangle_position[2],s =300,  marker="^",color='Yellow')
                self.canvas.axes.scatter(self.StoragePos1[0], self.StoragePos1[1],self.StoragePos1[2],s=400, marker="s",color='Blue')
                self.canvas.axes.scatter(self.StoragePos2[0], self.StoragePos2[1],self.StoragePos2[2],s=400, marker="o",color='Green')
                self.canvas.axes.scatter(self.StoragePos3[0], self.StoragePos3[1],self.StoragePos3[2],s=400, marker="^",color='yellow')
                self.canvas.axes.text(self.StoragePos2[0], self.StoragePos2[1],self.StoragePos2[2]+3,'STORAGE',fontsize=12,color='black')
                self.canvas.axes.plot([0,x[0]],[0,y[0]],[-5,z[0]], linewidth=10)
                self.canvas.axes.plot([x[0],x[1]],[y[0],y[1]],[z[0],z[1]], linewidth=9)
                self.canvas.axes.plot([x[1],x[2]],[y[1],y[2]],[z[1],z[2]],linewidth=9)
                self.canvas.axes.plot([x[2],x[3]],[y[2],y[3]],[z[2],z[3]],linewidth=9)
                self.canvas.axes.plot([x[3],x[4]],[y[3],y[4]],[z[3],z[4]],linewidth=9)
                self.canvas.axes.plot([x[4],x[5]],[y[4],y[5]],[z[4],z[5]],linewidth=9,color='red')
                self.canvas.axes.plot([x[5],x[6]],[y[5],y[6]],[z[5],z[6]],linestyle='dashed',linewidth=9)
    
                self.canvas.axes.scatter(0, 0, -5,color='k', marker="s",s=350)
                self.canvas.axes.scatter(x[0], y[0], z[0], marker="o", color='k',s=200)
                self.canvas.axes.scatter(x[1], y[1], z[1], marker="o", color='k',s=200)
                self.canvas.axes.scatter(x[2], y[2], z[2], marker="o", color='k',s=200)
                self.canvas.axes.scatter(x[3], y[3], z[3], marker="o", color='k',s=200)
                self.canvas.axes.scatter(x[4], y[4], z[4], marker="o", color='k',s=200)
                self.canvas.axes.scatter(x[5], y[5], z[5], marker="o", color='k',s=200)
                self.canvas.axes.scatter(x[6], y[6],z[6],s=150, marker="o",color='orange')
                self.canvas.draw()
                self.valuethe1.setText(str(round(self.the1_flex,4)))
                self.valuethe2.setText(str(round(self.the2_flex,4)))
                self.valuethe3.setText(str(round(self.the3_flex,4)))
                self.valuethe4.setText(str(round(self.the4_flex,4)))
                self.valuethe5.setText(str(round(self.the5_flex,4)))
                self.valuethe6.setText(str(round(self.the6_flex,4)))
                self.the1pre = self.the1_flex
                self.the2pre = self.the2_flex
                self.the3pre = self.the3_flex
                self.the4pre = self.the4_flex
                self.the5pre = self.the5_flex
                self.the6pre = self.the6_flex
                self.idx += 1
            except:
                pass

    def pick_up_square(self):
        self.idx_s=0
        while self.mode_check.isChecked() and self.idx_s <= self.time_respond.value()*10-30 and self.active_s == True:
            try:
                #self.timeqh = self.time_respond.value()*10
                tc = self.time_respond.value()
                x = float(self.xposvalue.text())
                y = float(self.yposvalue.text())
                z = float(self.zposvalue.text())
                yaw = float(self.yaw_value.text())
                pitch = float(self.pitch_value.text())
                roll = float(self.roll_value.text())
                the = np.round_(UIFunctions.inverse_kinematic(x,y,z,yaw,pitch,roll),5)
                a1 = self.the1pre
                b1 = 0
                c1 = 3 * (the[0]- self.the1pre) / tc ** 2
                d1 = -2 * (the[0] - self.the1pre) / tc ** 3
    
                a2 = self.the2pre
                b2 = 0
                c2 = 3 * (the[1]- self.the2pre) / tc ** 2
                d2 = -2 * (the[1]- self.the2pre) / tc ** 3
    
                a3 = self.the3pre
                b3 = 0
                c3 = 3 * (the[2] - self.the3pre) / tc ** 2
                d3 = -2 * (the[2] - self.the3pre) / tc ** 3
    
                a4 = self.the4pre
                b4 = 0
                c4 = 3 * (the[3] - self.the4pre) / tc ** 2
                d4 = -2 * (the[3] - self.the4pre) / tc ** 3
    
                a5 = self.the5pre
                b5 = 0
                c5 = 3 * (the[4] - self.the5pre) / tc ** 2
                d5 = -2 * (the[4] - self.the5pre) / tc ** 3
    
                a6 = self.the6pre
                b6 = 0
                c6 = 3 * (the[5]- self.the6pre) /tc ** 2
                d6 = -2 * (the[5] - self.the6pre) / tc ** 3
                self.label_time2.setText('Response Time:   '+str(float(self.idx_s/10))+'s')
                self.the1_flex = np.round(a1 + b1 * self.idx_s / 10 + c1 * (self.idx_s / 10) * 2 + d1 * (self.idx_s / 10) * 3, 4)
                self.the2_flex = np.round(a2 + b2 * self.idx_s / 10 + c2 * (self.idx_s / 10) * 2 + d2 * (self.idx_s / 10) * 3, 4)
                self.the3_flex = np.round(a3 + b3 * self.idx_s / 10 + c3 * (self.idx_s / 10) * 2 + d3 * (self.idx_s / 10) * 3, 4)
                self.the4_flex = np.round(a4 + b4 * self.idx_s / 10 + c4 * (self.idx_s / 10) * 2 + d4 * (self.idx_s / 10) * 3, 4)
                self.the5_flex = np.round(a5 + b5 * self.idx_s / 10 + c5 * (self.idx_s / 10) * 2 + d5 * (self.idx_s / 10) * 3, 4)
                self.the6_flex = np.round(a6 + b6 * self.idx_s / 10 + c6 * (self.idx_s / 10) * 2 + d6 * (self.idx_s / 10) * 3, 4)

                theta_flex = np.array([self.the1_flex,self.the2_flex,self.the3_flex,self.the4_flex,self.the5_flex,self.the6_flex])
                x,y,z = UIFunctions.forward_kinemtic_draw(theta_flex)
                self.current_x.setText(str(round(x[6],3)))
                self.current_y.setText(str(round(y[6],3)))
                self.current_z.setText(str(round(z[6],3)))
                self.canvas.axes.clear()
                self.canvas.axes.set_xlim(10,-45)
                self.canvas.axes.set_ylim(-45, 35)
                self.canvas.axes.set_zlim(-5, 35)
                self.canvas.axes.set_xlabel('X_axis',color='white',fontsize=10)
                self.canvas.axes.set_ylabel('Y_axis',color='white',fontsize=10)
                self.canvas.axes.set_zlabel('Z_axis',color='white',fontsize=10)
                self.canvas.axes.tick_params(axis='x', colors='white')
                self.canvas.axes.tick_params(axis='y', colors='white')
                self.canvas.axes.tick_params(axis='z', colors='white')
                if self.cylinder_position[0] < 9999 and self.cylinder_position[1] < 9999:
                    self.canvas.axes.scatter(self.cylinder_position[0], self.cylinder_position[1],
                                              self.cylinder_position[2],s =300,  marker="o",color='Green')
                if self.triangle_position[0] < 9999 and self.triangle_position[1] < 9999:
                    self.canvas.axes.scatter(self.triangle_position[0], self.triangle_position[1],
                                              self.triangle_position[2],s =300,  marker="^",color='Yellow')
                self.canvas.axes.scatter(self.StoragePos1[0], self.StoragePos1[1],self.StoragePos1[2],s=400, marker="s",color='Blue')
                self.canvas.axes.scatter(self.StoragePos2[0], self.StoragePos2[1],self.StoragePos2[2],s=400, marker="o",color='Green')
                self.canvas.axes.scatter(self.StoragePos3[0], self.StoragePos3[1],self.StoragePos3[2],s=400, marker="^",color='yellow')
                self.canvas.axes.text(self.StoragePos2[0], self.StoragePos2[1],self.StoragePos2[2]+3,'STORAGE',fontsize=12,color='black')
                self.canvas.axes.plot([0,x[0]],[0,y[0]],[-5,z[0]], linewidth=10)
                self.canvas.axes.plot([x[0],x[1]],[y[0],y[1]],[z[0],z[1]], linewidth=9)
                self.canvas.axes.plot([x[1],x[2]],[y[1],y[2]],[z[1],z[2]],linewidth=9)
                self.canvas.axes.plot([x[2],x[3]],[y[2],y[3]],[z[2],z[3]],linewidth=9)
                self.canvas.axes.plot([x[3],x[4]],[y[3],y[4]],[z[3],z[4]],linewidth=9)
                self.canvas.axes.plot([x[4],x[5]],[y[4],y[5]],[z[4],z[5]],linewidth=9,color='red')
                self.canvas.axes.plot([x[5],x[6]],[y[5],y[6]],[z[5],z[6]],linestyle='dashed',linewidth=9)
    
                self.canvas.axes.scatter(0, 0, -5,color='k', marker="s",s=350)
                self.canvas.axes.scatter(x[0], y[0], z[0], marker="o", color='k',s=200)
                self.canvas.axes.scatter(x[1], y[1], z[1], marker="o", color='k',s=200)
                self.canvas.axes.scatter(x[2], y[2], z[2], marker="o", color='k',s=200)
                self.canvas.axes.scatter(x[3], y[3], z[3], marker="o", color='k',s=200)
                self.canvas.axes.scatter(x[4], y[4], z[4], marker="o", color='k',s=200)
                self.canvas.axes.scatter(x[5], y[5], z[5], marker="o", color='k',s=200)
                self.canvas.axes.scatter(x[6], y[6],z[6],s =300,marker="s",color='Blue')
                self.canvas.draw()
                self.valuethe1.setText(str(round(self.the1_flex,4)))
                self.valuethe2.setText(str(round(self.the2_flex,4)))
                self.valuethe3.setText(str(round(self.the3_flex,4)))
                self.valuethe4.setText(str(round(self.the4_flex,4)))
                self.valuethe5.setText(str(round(self.the5_flex,4)))
                self.valuethe6.setText(str(round(self.the6_flex,4)))
                self.the1pre = self.the1_flex
                self.the2pre = self.the2_flex
                self.the3pre = self.the3_flex
                self.the4pre = self.the4_flex
                self.the5pre = self.the5_flex
                self.the6pre = self.the6_flex
                self.idx_s += 1
            except:
                pass
    def pick_up_circle(self):
        self.idx_c=0
        while self.mode_check.isChecked() and self.idx_c <= self.time_respond.value()*10-30 and self.active_c == True:
            try:
                #self.timeqh = self.time_respond.value()*10
                tc = self.time_respond.value()
                x = float(self.xposvalue.text())
                y = float(self.yposvalue.text())
                z = float(self.zposvalue.text())
                yaw = float(self.yaw_value.text())
                pitch = float(self.pitch_value.text())
                roll = float(self.roll_value.text())
                the = np.round_(UIFunctions.inverse_kinematic(x,y,z,yaw,pitch,roll),5)
                a1 = self.the1pre
                b1 = 0
                c1 = 3 * (the[0]- self.the1pre) / tc ** 2
                d1 = -2 * (the[0] - self.the1pre) / tc ** 3
    
                a2 = self.the2pre
                b2 = 0
                c2 = 3 * (the[1]- self.the2pre) / tc ** 2
                d2 = -2 * (the[1]- self.the2pre) / tc ** 3
    
                a3 = self.the3pre
                b3 = 0
                c3 = 3 * (the[2] - self.the3pre) / tc ** 2
                d3 = -2 * (the[2] - self.the3pre) / tc ** 3
    
                a4 = self.the4pre
                b4 = 0
                c4 = 3 * (the[3] - self.the4pre) / tc ** 2
                d4 = -2 * (the[3] - self.the4pre) / tc ** 3
    
                a5 = self.the5pre
                b5 = 0
                c5 = 3 * (the[4] - self.the5pre) / tc ** 2
                d5 = -2 * (the[4] - self.the5pre) / tc ** 3
    
                a6 = self.the6pre
                b6 = 0
                c6 = 3 * (the[5]- self.the6pre) /tc ** 2
                d6 = -2 * (the[5] - self.the6pre) / tc ** 3
                self.label_time2.setText('Response Time:   '+str(float(self.idx_c/10))+'s')
                self.the1_flex = np.round(a1 + b1 * self.idx_c / 10 + c1 * (self.idx_c / 10) * 2 + d1 * (self.idx_c / 10) * 3, 4)
                self.the2_flex = np.round(a2 + b2 * self.idx_c / 10 + c2 * (self.idx_c / 10) * 2 + d2 * (self.idx_c / 10) * 3, 4)
                self.the3_flex = np.round(a3 + b3 * self.idx_c / 10 + c3 * (self.idx_c / 10) * 2 + d3 * (self.idx_c / 10) * 3, 4)
                self.the4_flex = np.round(a4 + b4 * self.idx_c / 10 + c4 * (self.idx_c / 10) * 2 + d4 * (self.idx_c / 10) * 3, 4)
                self.the5_flex = np.round(a5 + b5 * self.idx_c / 10 + c5 * (self.idx_c / 10) * 2 + d5 * (self.idx_c / 10) * 3, 4)
                self.the6_flex = np.round(a6 + b6 * self.idx_c / 10 + c6 * (self.idx_c / 10) * 2 + d6 * (self.idx_c / 10) * 3, 4)

                theta_flex = np.array([self.the1_flex,self.the2_flex,self.the3_flex,self.the4_flex,self.the5_flex,self.the6_flex])
                x,y,z = UIFunctions.forward_kinemtic_draw(theta_flex)
                self.current_x.setText(str(round(x[6],3)))
                self.current_y.setText(str(round(y[6],3)))
                self.current_z.setText(str(round(z[6],3)))
                self.canvas.axes.clear()
                self.canvas.axes.set_xlim(10,-45)
                self.canvas.axes.set_ylim(-45, 35)
                self.canvas.axes.set_zlim(-5, 35)
                self.canvas.axes.set_xlabel('X_axis',color='white',fontsize=10)
                self.canvas.axes.set_ylabel('Y_axis',color='white',fontsize=10)
                self.canvas.axes.set_zlabel('Z_axis',color='white',fontsize=10)
                self.canvas.axes.tick_params(axis='x', colors='white')
                self.canvas.axes.tick_params(axis='y', colors='white')
                self.canvas.axes.tick_params(axis='z', colors='white')
                if  self.square_position[0] < 9999 and self.square_position[1] < 9999:
                    self.canvas.axes.scatter(self.square_position[0], self.square_position[1],
                                             self.square_position[2],s =300,marker="s",color='Blue')
                if self.triangle_position[0] < 9999 and self.triangle_position[1] < 9999:
                    self.canvas.axes.scatter(self.triangle_position[0], self.triangle_position[1],
                                              self.triangle_position[2],s =300,  marker="^",color='Yellow')
                self.canvas.axes.scatter(self.StoragePos1[0], self.StoragePos1[1],self.StoragePos1[2],s=400, marker="s",color='Blue')
                self.canvas.axes.scatter(self.StoragePos2[0], self.StoragePos2[1],self.StoragePos2[2],s=400, marker="o",color='Green')
                self.canvas.axes.scatter(self.StoragePos3[0], self.StoragePos3[1],self.StoragePos3[2],s=400, marker="^",color='yellow')
                self.canvas.axes.text(self.StoragePos2[0], self.StoragePos2[1],self.StoragePos2[2]+3,'STORAGE',fontsize=12,color='black')
                self.canvas.axes.plot([0,x[0]],[0,y[0]],[-5,z[0]], linewidth=10)
                self.canvas.axes.plot([x[0],x[1]],[y[0],y[1]],[z[0],z[1]], linewidth=9)
                self.canvas.axes.plot([x[1],x[2]],[y[1],y[2]],[z[1],z[2]],linewidth=9)
                self.canvas.axes.plot([x[2],x[3]],[y[2],y[3]],[z[2],z[3]],linewidth=9)
                self.canvas.axes.plot([x[3],x[4]],[y[3],y[4]],[z[3],z[4]],linewidth=9)
                self.canvas.axes.plot([x[4],x[5]],[y[4],y[5]],[z[4],z[5]],linewidth=9,color='red')
                self.canvas.axes.plot([x[5],x[6]],[y[5],y[6]],[z[5],z[6]],linestyle='dashed',linewidth=9)
    
                self.canvas.axes.scatter(0, 0, -5,color='k', marker="s",s=350)
                self.canvas.axes.scatter(x[0], y[0], z[0], marker="o", color='k',s=200)
                self.canvas.axes.scatter(x[1], y[1], z[1], marker="o", color='k',s=200)
                self.canvas.axes.scatter(x[2], y[2], z[2], marker="o", color='k',s=200)
                self.canvas.axes.scatter(x[3], y[3], z[3], marker="o", color='k',s=200)
                self.canvas.axes.scatter(x[4], y[4], z[4], marker="o", color='k',s=200)
                self.canvas.axes.scatter(x[5], y[5], z[5], marker="o", color='k',s=200)
                self.canvas.axes.scatter(x[6], y[6],z[6],s =300,marker="o",color='Green')
                self.canvas.draw()
                self.valuethe1.setText(str(round(self.the1_flex,4)))
                self.valuethe2.setText(str(round(self.the2_flex,4)))
                self.valuethe3.setText(str(round(self.the3_flex,4)))
                self.valuethe4.setText(str(round(self.the4_flex,4)))
                self.valuethe5.setText(str(round(self.the5_flex,4)))
                self.valuethe6.setText(str(round(self.the6_flex,4)))
                self.the1pre = self.the1_flex
                self.the2pre = self.the2_flex
                self.the3pre = self.the3_flex
                self.the4pre = self.the4_flex
                self.the5pre = self.the5_flex
                self.the6pre = self.the6_flex
                self.idx_c += 1
            except:
                pass
    def pick_up_triangle(self):
        self.idx_t = 0
        while self.mode_check.isChecked() and self.idx_t <= self.time_respond.value()*10-30 and self.active_t == True:
            try:
                tc = self.time_respond.value()
                x = float(self.xposvalue.text())
                y = float(self.yposvalue.text())
                z = float(self.zposvalue.text())
                yaw = float(self.yaw_value.text())
                pitch = float(self.pitch_value.text())
                roll = float(self.roll_value.text())
                the = np.round_(UIFunctions.inverse_kinematic(x,y,z,yaw,pitch,roll),5)
                a1 = self.the1pre
                b1 = 0
                c1 = 3 * (the[0]- self.the1pre) / tc ** 2
                d1 = -2 * (the[0] - self.the1pre) / tc ** 3
    
                a2 = self.the2pre
                b2 = 0
                c2 = 3 * (the[1]- self.the2pre) / tc ** 2
                d2 = -2 * (the[1]- self.the2pre) / tc ** 3
    
                a3 = self.the3pre
                b3 = 0
                c3 = 3 * (the[2] - self.the3pre) / tc ** 2
                d3 = -2 * (the[2] - self.the3pre) / tc ** 3
    
                a4 = self.the4pre
                b4 = 0
                c4 = 3 * (the[3] - self.the4pre) / tc ** 2
                d4 = -2 * (the[3] - self.the4pre) / tc ** 3
    
                a5 = self.the5pre
                b5 = 0
                c5 = 3 * (the[4] - self.the5pre) / tc ** 2
                d5 = -2 * (the[4] - self.the5pre) / tc ** 3
    
                a6 = self.the6pre
                b6 = 0
                c6 = 3 * (the[5]- self.the6pre) /tc ** 2
                d6 = -2 * (the[5] - self.the6pre) / tc ** 3
                self.label_time2.setText('Response Time:   '+str(float(self.idx_t/10))+'s')
                self.the1_flex = np.round(a1 + b1 * self.idx_t / 10 + c1 * (self.idx_t / 10) * 2 + d1 * (self.idx_t / 10) * 3, 4)
                self.the2_flex = np.round(a2 + b2 * self.idx_t / 10 + c2 * (self.idx_t / 10) * 2 + d2 * (self.idx_t / 10) * 3, 4)
                self.the3_flex = np.round(a3 + b3 * self.idx_t / 10 + c3 * (self.idx_t / 10) * 2 + d3 * (self.idx_t / 10) * 3, 4)
                self.the4_flex = np.round(a4 + b4 * self.idx_t / 10 + c4 * (self.idx_t / 10) * 2 + d4 * (self.idx_t / 10) * 3, 4)
                self.the5_flex = np.round(a5 + b5 * self.idx_t / 10 + c5 * (self.idx_t / 10) * 2 + d5 * (self.idx_t / 10) * 3, 4)
                self.the6_flex = np.round(a6 + b6 * self.idx_t / 10 + c6 * (self.idx_t / 10) * 2 + d6 * (self.idx_t / 10) * 3, 4)

                theta_flex = np.array([self.the1_flex,self.the2_flex,self.the3_flex,self.the4_flex,self.the5_flex,self.the6_flex])
                x,y,z = UIFunctions.forward_kinemtic_draw(theta_flex)
                self.current_x.setText(str(round(x[6],3)))
                self.current_y.setText(str(round(y[6],3)))
                self.current_z.setText(str(round(z[6],3)))
                self.canvas.axes.clear()
                self.canvas.axes.set_xlim(10,-45)
                self.canvas.axes.set_ylim(-45, 35)
                self.canvas.axes.set_zlim(-5, 35)
                self.canvas.axes.set_xlabel('X_axis',color='white',fontsize=10)
                self.canvas.axes.set_ylabel('Y_axis',color='white',fontsize=10)
                self.canvas.axes.set_zlabel('Z_axis',color='white',fontsize=10)
                self.canvas.axes.tick_params(axis='x', colors='white')
                self.canvas.axes.tick_params(axis='y', colors='white')
                self.canvas.axes.tick_params(axis='z', colors='white')
                if  self.square_position[0] < 9999 and self.square_position[1] < 9999:
                    self.canvas.axes.scatter(self.square_position[0], self.square_position[1],
                                             self.square_position[2],s =300,marker="s",color='Blue')
                if self.cylinder_position[0] < 9999 and self.cylinder_position[1] < 9999:
                    self.canvas.axes.scatter(self.cylinder_position[0], self.cylinder_position[1],
                                              self.cylinder_position[2],s =300,marker="o",color='Green')
                self.canvas.axes.scatter(self.StoragePos1[0], self.StoragePos1[1],self.StoragePos1[2],s=400, marker="s",color='Blue')
                self.canvas.axes.scatter(self.StoragePos2[0], self.StoragePos2[1],self.StoragePos2[2],s=400, marker="o",color='Green')
                self.canvas.axes.scatter(self.StoragePos3[0], self.StoragePos3[1],self.StoragePos3[2],s=400, marker="^",color='yellow')
                self.canvas.axes.text(self.StoragePos2[0], self.StoragePos2[1],self.StoragePos2[2]+3,'STORAGE',fontsize=12,color='black')
                self.canvas.axes.plot([0,x[0]],[0,y[0]],[-5,z[0]], linewidth=10)
                self.canvas.axes.plot([x[0],x[1]],[y[0],y[1]],[z[0],z[1]], linewidth=9)
                self.canvas.axes.plot([x[1],x[2]],[y[1],y[2]],[z[1],z[2]],linewidth=9)
                self.canvas.axes.plot([x[2],x[3]],[y[2],y[3]],[z[2],z[3]],linewidth=9)
                self.canvas.axes.plot([x[3],x[4]],[y[3],y[4]],[z[3],z[4]],linewidth=9)
                self.canvas.axes.plot([x[4],x[5]],[y[4],y[5]],[z[4],z[5]],linewidth=9,color='red')
                self.canvas.axes.plot([x[5],x[6]],[y[5],y[6]],[z[5],z[6]],linestyle='dashed',linewidth=9)
    
                self.canvas.axes.scatter(0, 0, -5,color='k', marker="s",s=350)
                self.canvas.axes.scatter(x[0], y[0], z[0], marker="o", color='k',s=200)
                self.canvas.axes.scatter(x[1], y[1], z[1], marker="o", color='k',s=200)
                self.canvas.axes.scatter(x[2], y[2], z[2], marker="o", color='k',s=200)
                self.canvas.axes.scatter(x[3], y[3], z[3], marker="o", color='k',s=200)
                self.canvas.axes.scatter(x[4], y[4], z[4], marker="o", color='k',s=200)
                self.canvas.axes.scatter(x[5], y[5], z[5], marker="o", color='k',s=200)
                self.canvas.axes.scatter(x[6], y[6],z[6],s =300,marker="^",color='Yellow')
                self.canvas.draw()
                self.valuethe1.setText(str(round(self.the1_flex,4)))
                self.valuethe2.setText(str(round(self.the2_flex,4)))
                self.valuethe3.setText(str(round(self.the3_flex,4)))
                self.valuethe4.setText(str(round(self.the4_flex,4)))
                self.valuethe5.setText(str(round(self.the5_flex,4)))
                self.valuethe6.setText(str(round(self.the6_flex,4)))
                self.the1pre = self.the1_flex
                self.the2pre = self.the2_flex
                self.the3pre = self.the3_flex
                self.the4pre = self.the4_flex
                self.the5pre = self.the5_flex
                self.the6pre = self.the6_flex
                self.idx_t += 1
            except:
                pass
    def audio_information_start(self):
        if self.active_audio == True:
            (self.sr,self.signal) = read_wavfile('record.wav')
            mfcc_feat = feature_extract(self.signal, self.sr)
            winlen=0.025
            winstep=0.01
            Frame_len = winlen*self.sr
            FrameStep = winstep*self.sr
            num_frames = int(np.ceil(float(np.abs(len(self.signal) - Frame_len)) / FrameStep))
            
            self.cepstral_coefficents,self.pspec,feat,log_bank,frames = mfcc(self.signal,self.sr,winlen,winstep,numcep=13,
                     nfilt=26,nfft=512,lowfreq=0,highfreq=None,fcut = 3000,ceplifter=22,open_lift = True,
                     winfunc="hamming",sum_up = True,appendEnergy=True)
            self.samples = feature_extract(self.signal,self.sr)
            self.tfrm= np.arange(Frame_len/2,Frame_len/2+(num_frames)*FrameStep,FrameStep,dtype=float)/self.sr
            rows,cols= np.shape(self.pspec)
            self.Freq = np.linspace(0,(self.sr)*(1-1/cols)/1000,cols)
            self.duration = np.dot(self.sr,(np.arange(0, len(self.signal))/len(self.signal)))
            
            self.canvas_spec.axes.clear()
            self.canvas_spec.axes.tick_params(axis='x', colors='white')
            self.canvas_spec.axes.tick_params(axis='y', colors='white')
            self.canvas_spec.axes.tick_params(axis='z', colors='white')
            surf = self.canvas_spec.axes.plot_surface( self.tfrm[:, None],self.Freq[None,:],10.0*np.log10(self.pspec), cmap=cm.jet,linewidth=5)
            self.canvas_spec.axes.set_xlabel('Time(s)-Domain',color='white',fontsize=8)
            self.canvas_spec.axes.set_ylabel('Frequency(Hz)-Domain',color='white',fontsize=8)
            self.canvas_spec.axes.set_zlabel('Amplitude(DB)',color='white',fontsize=8)
            self.canvas_spec.draw()
            
            self.canvas_mfcc.ax.clear()
            self.canvas_mfcc.ax.set_xlabel('time',)
            self.canvas_mfcc.ax.xaxis.label.set_color('white')
            self.canvas_mfcc.ax.grid(True)
            self.canvas_mfcc.ax.tick_params(axis='x', colors='white')
            self.canvas_mfcc.ax.tick_params(axis='y', colors='white')
            self.canvas_mfcc.ax.plot(np.linspace(0, len(self.samples), num=len(self.samples)), self.samples,antialiased=False,color="C0")
            self.canvas_mfcc.draw()
            
            self.canvas_record.ax.clear()
            self.canvas_record.ax.grid(True)
            self.canvas_record.ax.tick_params(axis='x', colors='white')
            self.canvas_record.ax.tick_params(axis='y', colors='white')
            self.canvas_record.ax.plot(self.signal,color="C0")
            self.canvas_record.ax.yaxis.grid(True,linestyle='--')
            self.canvas_record.ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
            self.canvas_record.draw()
        else:
            pass
    def start_pick_function(self):
        try:
            if self.block_name.currentText().strip() =='hình vuông':
                xpos = round(float(self.rasp_xpos.text()),1)
                ypos = round(float(self.rasp_ypos.text()),1)
                zpos = round(float(self.rasp_zpos.text()),1)
                pitch = roll = 0
                yaw = self.angle_square
                self.stop_worker_mode()
                UIFunctions.send(self,xpos,ypos,zpos,yaw,pitch,roll)
                self.start_pick_up_square()
                time.sleep(self.time_respond.value())
                self.stop_pick_up_square()
                yaw=0; pitch =0 ;roll = 0
                UIFunctions.send(self,self.StoragePos1[0],self.StoragePos1[1],self.StoragePos1[2]+10,yaw,pitch,roll)
                self.start_pick_up_square()
                time.sleep(self.time_respond.value())
                self.stop_pick_up_square()
            elif self.block_name.currentText().strip() == 'hình tròn':
                xpos = round(float(self.rasp_xpos.text()),1)
                ypos = round(float(self.rasp_ypos.text()),1)
                zpos = round(float(self.rasp_zpos.text()),1)
                yaw =0; pitch =90; roll = 0
                self.stop_worker_mode()
                UIFunctions.send(self,xpos,ypos,zpos,yaw,pitch,roll)
                self.start_pick_up_circle()
                time.sleep(self.time_respond.value())
                self.stop_pick_up_circle()
                yaw=0; pitch =0 ;roll = 0
                UIFunctions.send(self,self.StoragePos2[0],self.StoragePos2[1],self.StoragePos2[2]+10,yaw,pitch,roll)
                self.start_pick_up_circle()
                time.sleep(self.time_respond.value())
                self.stop_pick_up_circle()
            elif self.block_name.currentText().strip() == 'tam giác':
                
                xpos = round(float(self.rasp_xpos.text()),1)
                ypos = round(float(self.rasp_ypos.text()),1)
                zpos = round(float(self.rasp_zpos.text()),1)
                yaw =0; pitch =45;
                roll = self.angle_triangle
                UIFunctions.send(self,xpos,ypos,zpos,yaw,pitch,roll)
                self.start_pick_up_triangle()
                time.sleep(self.time_respond.value())
                self.stop_pick_up_triangle()
                yaw=0; pitch =0 ;roll = 0
                UIFunctions.send(self,self.StoragePos3[0],self.StoragePos3[1],self.StoragePos3[2]+10,yaw,pitch,roll)
                self.start_pick_up_triangle()
                time.sleep(self.time_respond.value())
                self.stop_pick_up_triangle()
        except:
            x = -11.8
            y = 0.0
            z = 13.1
            yaw=0; pitch =0 ;roll = 0
            self.stop_pick_up_square()
            self.stop_pick_up_circle()
            self.stop_pick_up_triangle()
            self.stop_worker_mode()
            UIFunctions.send(self,x,y,z,yaw,pitch,roll)
            self.start_worker_mode()
            time.sleep(self.time_respond.value())
    def start_drop_function(self):
        try:
            if self.block_name.currentText().strip() =='hình vuông':
                yaw = pitch = roll = 0 
                UIFunctions.send(self,self.StoragePos1[0],self.StoragePos1[1],self.StoragePos1[2],yaw,pitch,roll)
                self.start_pick_up_square()
                time.sleep(self.time_respond.value())
                self.stop_pick_up_square()
            elif self.block_name.currentText().strip() == 'hình tròn':
                yaw =0; pitch =0; roll = 0
                UIFunctions.send(self,self.StoragePos2[0],self.StoragePos2[1],self.StoragePos2[2],yaw,pitch,roll)
                self.start_pick_up_circle()
                time.sleep(self.time_respond.value())
                self.stop_pick_up_circle()
            elif self.block_name.currentText().strip() == 'tam giác':
                yaw =0; pitch =0; roll = 0
                UIFunctions.send(self,self.StoragePos3[0],self.StoragePos3[1],self.StoragePos3[2],yaw,pitch,roll)
                self.start_pick_up_triangle()
                time.sleep(self.time_respond.value())
                self.stop_pick_up_triangle()
            x = -11.8
            y = 0.0
            z = 13.1
            yaw=0; pitch =0 ;roll = 0
            UIFunctions.send(self,x,y,z,yaw,pitch,roll)
            self.start_worker_mode()
            time.sleep(self.time_respond.value())
        except:
            x = -11.8
            y = 0.0
            z = 13.1
            yaw=0; pitch =0 ;roll = 0
            self.stop_pick_up_square()
            self.stop_pick_up_circle()
            self.stop_pick_up_triangle()
            self.stop_worker_mode()
            UIFunctions.send(self,x,y,z,yaw,pitch,roll)
            self.start_worker_mode()
            time.sleep(self.time_respond.value())
class Worker(QtCore.QRunnable):

	def __init__(self, function, *args, **kwargs):
		super(Worker, self).__init__()
		self.function = function
		self.args = args
		self.kwargs = kwargs

	@pyqtSlot()
	def run(self):

		self.function(*self.args, **self.kwargs)		
class Slash_screen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = uic.loadUi('splash_screen.ui',self)
                
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    
    
        ## DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)
        self.ui.btn_load.setEnabled(False)
        ## QTIMER ==> START
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        # TIMER IN MILLISECONDS
        self.timer.start(25)
        self.ui.label_description.setText("<strong>WELCOME</strong> To Seminar Project")
        self.ui.label_sys.setText('System: ' + platform.system())
        self.ui.label_sys.adjustSize()
        self.ui.label_version.setText('Version of System: ' + platform.release())
        self.ui.label_version.adjustSize()
        QtCore.QTimer.singleShot(1500, lambda: self.ui.label_description.setText("<strong>LOADING</strong> database"))
        # Change Texts
        QtCore.QTimer.singleShot(1500, lambda: self.ui.label_description.setText("<strong>LOADING</strong> privacy policy"))
        QtCore.QTimer.singleShot(2000, lambda: self.ui.label_description.setText("<strong>LOADING</strong> login screen"))
        QtCore.QTimer.singleShot(2000, lambda: self.ui.label_description.setText("<strong>LOADING</strong> manual control"))
        QtCore.QTimer.singleShot(3000, lambda: self.ui.label_description.setText("<strong>LOADING</strong> recoding function"))
        QtCore.QTimer.singleShot(3000, lambda: self.ui.label_description.setText("<strong>LOADING</strong> neural network model"))
        QtCore.QTimer.singleShot(3500, lambda: self.ui.label_description.setText("<strong>Creating....."))
        
    def progress(self):
    
            global counter
    
            # SET VALUE TO PROGRESS BAR
            self.ui.progressBar.setValue(counter)
    
            if counter > 100:
                # STOP TIMER
                self.timer.stop()
                self.ui.btn_load.setText('START')
                self.ui.btn_load.setEnabled(True)
                self.ui.btn_load.clicked.connect(lambda: self.open_main())
            counter += 1
    def open_main(self):
        self.main = MainWindow()
        self.main.show()
        self.close()
        
class introduction(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = uic.loadUi('introduction.ui',self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons\24x24\cil-microphone.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowTitle('Introduction')
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.plainTextEdit.setGraphicsEffect(self.shadow)
        self.ui.btn_login.clicked.connect(lambda: self.close())
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Slash_screen()
    window.show()
    sys.exit(app.exec_())
