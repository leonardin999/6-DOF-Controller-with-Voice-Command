# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 16:25:10 2021

@author: Leonard
"""


from ui_styles import *
from GUI_Presentation import *
import fnmatch
import time
from module_function_GUI import *
from feature_extraction_GUI import *
import numpy as np
from pydub import AudioSegment
import math as m
import pyttsx3
import glob
from scipy.io import loadmat,savemat
import pandas as pd
from datetime import timedelta
import os
counter = 0
class UIFunctions(MainWindow):

    def toggleMenu(self, maxWidth, enable):
        if enable:
            self.Content_4.hide()
            self.Content.show()
            width = self.frame_left_menu.width()
            maxExtend = maxWidth
            standard = 10
            # 
            # SET MAX WIDTH
            if width == 10:
                self.start_worker_audio()
                widthExtended = maxExtend
                self.ui.resize(1796, 820)
                
            else:
                self.stop_worker_audio()
                widthExtended = standard
                self.ui.resize(1016, 820)
            # ANIMATION
            self.animation = QPropertyAnimation(self.frame_left_menu, b"minimumWidth")
            self.animation.setDuration(400)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()
    def toggleMenu_setting(self, maxWidth, enable):
        if enable:
            # GET WIDTH
            width = self.frame_left_menu_3.width()
            maxExtend = maxWidth
            standard = 65
            # 
            # SET MAX WIDTH
            if width == 65:
                
                self.groupBox_3.show()
                self.groupBox_4.show()
                self.groupBox_6.show()

                widthExtended = maxExtend
            else:
                self.groupBox_3.hide()
                self.groupBox_4.hide()
                self.groupBox_6.hide()
                widthExtended = standard
            # ANIMATION
            self.animation = QPropertyAnimation(self.frame_left_menu_3, b"minimumWidth")
            self.animation.setStartValue(width)
            self.animation.setDuration(450)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()
            
    def toggleMenu_analysis(self, maxWidth, enable):
        if enable:
            self.Content.hide()
            self.Content_4.show()
            width = self.frame_left_menu_5.width()
            maxExtend = maxWidth
            standard = 10
            # 
            # SET MAX WIDTH
            if width == 10:
                self.start_worker_audio()
                widthExtended = maxExtend
                self.ui.resize(1796, 820)
                
            else:
                self.stop_worker_audio()
                widthExtended = standard
                self.ui.resize(1016, 820)
            # ANIMATION
            self.animation = QPropertyAnimation(self.frame_left_menu_5, b"minimumWidth")
            self.animation.setDuration(400)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()
    def read_analysis(self):
        self.storage_quality = pd.read_csv('Data_analysis\Storage_exposed.csv')
        self.storage_quality.head()
        self.storage_quality["DateTime"] = pd.to_datetime(self.storage_quality["DateTime"])
        self.storage_quality.index = self.storage_quality["DateTime"]
        time = self.storage_quality["DateTime"]
        self.min_day.setText(str(time.min()))
        self.Max_day.setText(str(time.max()))
        self.delta_time.setText(str(time.max()- time.min()))
        
    def sumary_store(self):
        if self.choose_store.currentText() == "Storage1":
            total = sum(self.storage_quality["Storage1"])
            self.overall_val.setText(str(total))
        elif self.choose_store.currentText() == "Storage2":
            total = sum(self.storage_quality["Storage2"])
            self.overall_val.setText(str(total))
        elif self.choose_store.currentText() == "Storage3":
            total = sum(self.storage_quality["Storage3"])
            self.overall_val.setText(str(total))
        else:
            pass
    def plot_bar_chart(self):
        self.canvas_data2.axes.clear()
        if self.choose_store.currentText() == "Storage1":
            self.canvas_data2.axes.plot(self.storage_quality["Storage1"],color='red')
        elif self.choose_store.currentText() == "Storage2":
            self.canvas_data2.axes.plot(self.storage_quality["Storage2"],color='red')
        elif self.choose_store.currentText() == "Storage3":
            self.canvas_data2.axes.plot(self.storage_quality["Storage3"],color='red')
        else:
            pass
        self.canvas_data2.axes.tick_params(axis='y', colors='white')
        self.canvas_data2.axes.tick_params(axis='x', colors='white')
        self.canvas_data2.axes.grid(True)
        self.canvas_data2.draw()
    def open_file(self):
        os.startfile('Data_analysis\Storage_exposed.xlsx')
    def display_result(self):
        start_day = self.day_start.currentText()
        start_month= self.month_start.currentText()
        start_year= self.year_start.currentText()
        
        end_day = self.day_end.currentText()
        end_month= self.month_end.currentText()
        end_year= self.year_end.currentText()
        time1_df = start_day+'th'+' of'+' '+start_month+', '+start_year
        time2_df = end_day+'th'+' of'+' '+end_month+', '+end_year
        d1 = pd.to_datetime(time1_df)
        d2 = pd.to_datetime(time2_df)
        self.info = self.storage_quality[d1:d2]
        self.Store1_val.setText(str(sum(self.info['Storage1'])))
        self.Store2_val.setText(str(sum(self.info['Storage2'])))
        self.Store3_val.setText(str(sum(self.info['Storage3'])))
        self.total_val.setText(str(sum(self.info['Storage1']+self.info['Storage2']+self.info['Storage3'])))
        self.canvas_data1.axes.clear()
        self.canvas_data1.axes.plot(self.info['Storage1'],"-o")
        self.canvas_data1.axes.plot(self.info['Storage2'],"-o")
        self.canvas_data1.axes.plot(self.info['Storage3'],"-o")
        self.canvas_data1.axes.legend(labels=['Storage1', 'Storage1','Storage3'])
        self.canvas_data1.axes.tick_params(axis='y', colors='white')
        self.canvas_data1.axes.tick_params(axis='x', colors='white')
        self.canvas_data1.axes.grid(True)
        self.canvas_data1.draw()

    def set_up_voice(self):
        if  self.lis_assistant.currentText().strip() == 'David':
            self.engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')
        elif   self.lis_assistant.currentText().strip() == 'James':
            self.engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enAU_JamesM')
        elif  self.lis_assistant.currentText().strip() == 'Mark':
            self.engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enUS_MarkM')
        elif  self.lis_assistant.currentText().strip() == 'Catherine':
            self.engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enAU_CatherineM')
        elif  self.lis_assistant.currentText().strip() == 'Zira':
            self.engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
    def test_voices(self):
        self.engine.say("Hi There! my name is "+ self.lis_assistant.currentText() +",It's a pleasue to be your assistant "
           ". How can I help you out? ")
        self.engine.runAndWait()
        self.engine.stop()
        
    def setup_camera(self):
        if self.widget_2.isVisible():
            self.widget_2.hide()
            self.check_camera.setChecked(False)
        else:
            self.widget_2.show()
            self.check_camera.setChecked(True)
            
    def Record_toOpen(self):
        data_dir = pathlib.Path('audio folder/mini_speech_commands_Function')
        if not data_dir.exists():
            print('direction not found!')
        self.label_1 = np.array(os.listdir(str(data_dir)))
        ## from the model:
        data_dir_model = pathlib.Path('audio folder/coeffs_Function')
        if not data_dir_model.exists():
            print('direction not found!')
        filenames = glob.glob(str(data_dir_model)+'/*')
        self.weights_1 = model_load(filenames[1])
        self.Lambda_1 = model_load(filenames[0],'lambda')
        [command,percent] = record(self.weights_1,self.Lambda_1,self.label_1)
        if command.strip() == 'xin chào':
            self.check_audio.setChecked(True)
            self.label_26.setText('Accepted')
            self.engine.say("Welcome to DR3 robot Controller designed by DRC Laboratory!")
            self.engine.runAndWait()
            self.engine.stop()
        else:
            self.check_audio.setChecked(False)
            self.label_26.setText('Unaccepted')
            self.engine.say("Please try again")
            self.engine.runAndWait()
            self.engine.stop()
            
    def Record_toFunction(self):
        data_dir = pathlib.Path('audio folder/mini_speech_commands_Function')
        if not data_dir.exists():
            print('direction not found!')
        self.label_1 = np.array(os.listdir(str(data_dir)))
        ## from the model:
        data_dir_model = pathlib.Path('audio folder/coeffs_Function')
        if not data_dir_model.exists():
            print('direction not found!')
        filenames = glob.glob(str(data_dir_model)+'/*')
        self.engine.say(" Choosing controller Function to operate the robot!")
        self.engine.runAndWait()
        self.engine.stop()
        self.weights_1 = model_load(filenames[1])
        self.Lambda_1 = model_load(filenames[0],'lambda')
        [command,percent] = record(self.weights_1,self.Lambda_1,self.label_1)
        if command.strip() == 'autopilot':
            self.auto = True
            self.auto_man_check.setChecked(True)
            self.engine.say("Active Automative controller mode. Ready to recive your order!")
            self.engine.runAndWait()
            self.engine.stop()
            self.label_mode.setText('Mode: Auto-controller')
        elif command.strip() == 'hand control':
            self.manual = True
            self.auto_man_check.setChecked(True)
            self.engine.say("Active hand-on controller mode. Ready to recive your order!")
            self.engine.runAndWait()
            self.engine.stop()
            self.label_mode.setText('Mode: Manual-controller')
        else:
            self.auto = False
            self.manual = False
            self.auto_man_check.setChecked(False)
            self.engine.say("You may want to try again")
            self.engine.runAndWait()
            self.engine.stop()

    def Record_toManual(self):
        data_dir = pathlib.Path('audio folder/mini_speech_commands_Manual')
        if not data_dir.exists():
            print('direction not found!')
        self.label_2 = np.array(os.listdir(str(data_dir)))
        ## from the model:
        data_dir_model = pathlib.Path('audio folder/coeffs_Manual')
        if not data_dir_model.exists():
            print('direction not found!')
        filenames = glob.glob(str(data_dir_model)+'/*')
        self.weights_2 = model_load(filenames[1])
        self.Lambda_2 = model_load(filenames[0],'lambda')
        [command,percent] = record(self.weights_2,self.Lambda_2,self.label_2)
        self.accurate.setText(str(round(percent)))
        self.commandline.setText(command)
        if command.strip() == 'tạm biệt':
            self.check_audio.setChecked(False)
            self.auto_man_check.setChecked(False)
            self.auto = False
            self.manual = False
            self.label_mode.setText('Mode:          ')
            self.label_26.setText('Unaccepted')
            self.engine.say("Disable Manually controller. Goodbye!")
            self.engine.runAndWait()
            self.engine.stop()
        elif command.strip() == 'trái':
            UIFunctions.left_signal(self)
        elif command.strip() == 'tiến':
            UIFunctions.forward_signal(self) 
        elif command.strip() == 'lùi':
            UIFunctions.backward_signal(self)
        elif command.strip() == 'phải':
            UIFunctions.right_signal(self)
        elif command.strip() == 'lên':
            UIFunctions.up_signal(self)
        elif command.strip() == 'xuống':
            UIFunctions.down_signal(self)
        elif command.strip() == 'gắp':
             self.pick_function()
        elif command.strip() == 'thả':
            self.drop_function()
        
        else:
            self.accurate.clear()
            self.commandline.clear()
            self.engine.say("Please try again. Thank you!")
            self.engine.runAndWait()
            self.engine.stop()

    def Record_toAuto_confirm(self):
        data_dir = pathlib.Path('audio folder/mini_speech_commands_Auto_Update')
        if not data_dir.exists():
            print('direction not found!')
        self.label_3 = np.array(os.listdir(str(data_dir)))
        ## from the model:
        data_dir_model = pathlib.Path('audio folder/coeffs_Auto_Update')
        if not data_dir_model.exists():
            print('direction not found!')
        filenames = glob.glob(str(data_dir_model)+'/*')
        self.weights_3 = model_load(filenames[1])
        self.Lambda_3 = model_load(filenames[0],'lambda')
        self.engine.say("I'm listening.")
        self.engine.runAndWait()
        self.engine.stop()
        [command,percent] = record(self.weights_3,self.Lambda_3,self.label_3)
        self.accurate.setText(str(round(percent)))
        self.commandline.setText(command)
        if command.strip() == 'tạm biệt':
            self.check_audio.setChecked(False)
            self.auto_man_check.setChecked(False)
            self.auto = False
            self.manual = False
            self.label_mode.setText('Mode:          ')
            self.label_26.setText('Unaccepted')
            self.engine.say("Disable Automation controller. Goodbye!")
            self.engine.runAndWait()
            self.engine.stop()
        elif command.strip() == 'hình vuông':
            if float(self.accurate.text()) < 90.0:
                self.engine.say("Do you want to pick up a Rectangle block in the field")
                self.engine.runAndWait()
                self.engine.stop()
                data_dir_model = pathlib.Path('audio folder/coeffs_Auto_Update')
                data_dir = pathlib.Path('audio folder/mini_speech_commands_Auto_Update')
                self.label_confirm = np.array(os.listdir(str(data_dir)))
                filenames = glob.glob(str(data_dir_model)+'/*')
                self.weights_confirm = model_load(filenames[1])
                self.Lambda_confirm = model_load(filenames[0],'lambda')
                [confirm,_] = record(self.weights_confirm,self.Lambda_confirm,self.label_confirm)
                if confirm.strip() == 'yes':
                    index = self.block_name.findText(self.commandline.text(),QtCore.Qt.MatchFixedString)
                    self.block_name.setCurrentIndex(index)
                    self.start_worker_3()
                elif confirm.strip() == 'no':
                    self.engine.say("Ok")
                    self.engine.runAndWait()
                    self.engine.stop()
                else :
                    self.engine.say("You may want to try again!")
                    self.engine.runAndWait()
                    self.engine.stop()
            else:
                index = self.block_name.findText(self.commandline.text(),QtCore.Qt.MatchFixedString)
                self.block_name.setCurrentIndex(index)
                self.start_worker_3()
        elif command.strip() == 'hình tròn':
            if float(self.accurate.text()) < 93.0:
                self.engine.say("Do you want to pick up a Cylinder block in the field")
                self.engine.runAndWait()
                self.engine.stop()
                data_dir_model = pathlib.Path('audio folder/coeffs_Auto_Update')
                data_dir = pathlib.Path('audio folder/mini_speech_commands_Auto_Update')
                self.label_confirm = np.array(os.listdir(str(data_dir)))
                filenames = glob.glob(str(data_dir_model)+'/*')
                self.weights_confirm = model_load(filenames[1])
                self.Lambda_confirm = model_load(filenames[0],'lambda')
                [confirm,_] = record(self.weights_confirm,self.Lambda_confirm,self.label_confirm)
                if confirm.strip() == 'yes':
                    index = self.block_name.findText(self.commandline.text(),QtCore.Qt.MatchFixedString)
                    self.block_name.setCurrentIndex(index)
                    self.start_worker_3()
                elif confirm.strip() == 'no':
                    self.engine.say("Ok")
                    self.engine.runAndWait()
                    self.engine.stop()
                else :
                    self.engine.say("You may want to try again!")
                    self.engine.runAndWait()
                    self.engine.stop()
            else:
                index = self.block_name.findText(self.commandline.text(),QtCore.Qt.MatchFixedString)
                self.block_name.setCurrentIndex(index)
                self.start_worker_3()
        elif command.strip() == 'tam giác':
            if float(self.accurate.text()) < 93.0:
                self.engine.say("Do you want to pick up a Triangle block in the field")
                self.engine.runAndWait()
                self.engine.stop()
                data_dir_model = pathlib.Path('audio folder/coeffs_Auto_Update')
                data_dir = pathlib.Path('audio folder/mini_speech_commands_Auto_Update')
                self.label_confirm = np.array(os.listdir(str(data_dir)))
                filenames = glob.glob(str(data_dir_model)+'/*')
                self.weights_confirm = model_load(filenames[1])
                self.Lambda_confirm = model_load(filenames[0],'lambda')
                [confirm,_] = record(self.weights_confirm,self.Lambda_confirm,self.label_confirm)
                if confirm.strip() == 'yes':
                    index = self.block_name.findText(self.commandline.text(),QtCore.Qt.MatchFixedString)
                    self.block_name.setCurrentIndex(index)
                    self.start_worker_3()
                elif confirm.strip() == 'no':
                    self.engine.say("Ok")
                    self.engine.runAndWait()
                    self.engine.stop()
                else :
                    self.engine.say("You may want to try again!")
                    self.engine.runAndWait()
                    self.engine.stop()
            else:
                index = self.block_name.findText(self.commandline.text(),QtCore.Qt.MatchFixedString)
                self.block_name.setCurrentIndex(index)
                self.start_worker_3()

        else:
            self.accurate.clear()
            self.commandline.clear()
            self.engine.say("Please try again. Thank you!")
            self.engine.runAndWait()
            self.engine.stop()

    def ask_for_control(self):
        if not self.check_audio.isChecked():
            UIFunctions.Record_toOpen(self)
        elif self.check_audio.isChecked()== True and self.auto_man_check.isChecked()== False:
            UIFunctions.Record_toFunction(self)
        elif self.check_audio.isChecked()== True and self.auto_man_check.isChecked()== True:
            if self.auto == True:
                UIFunctions.Record_toAuto_confirm(self)
            elif self.manual == True:
                UIFunctions.Record_toManual(self)
    def showDialog(self):
        label = self.commandline.text()
        if label == 'hình vuông':
            say = 'square'
        elif label == 'hình tròn':
            say = 'circle'
        elif label == 'tam giác':
            say = 'triangle'
        self.engine.say("You want to pick up "+say+" in the Field?")
        self.engine.runAndWait()
        self.engine.stop()
        self.msgBox = QMessageBox()
        self.msgBox.setIcon(QMessageBox.Information)
        self.msgBox.setText("Pick up "+label+"?")
        self.msgBox.setWindowTitle("Confirmation")
        self.msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        returnValue = self.msgBox.exec()
        return returnValue
    def showDialog_start(self):
        self.engine.say("Do you want to Reset the current position of robot?")
        self.engine.runAndWait()
        self.engine.stop()
        self.msgBox = QMessageBox()
        self.msgBox.setIcon(QMessageBox.Information)
        self.msgBox.setText("Reset Position?")
        self.msgBox.setWindowTitle("Confirmation")
        self.msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        returnValue = self.msgBox.exec()
        return returnValue
    
    def Serial_connect(self,comm,baud):
        self.ser.port = comm
        self.ser.baudrate =  baud
        self.ser.bytesize = serial.EIGHTBITS #number of bits per bytes
        self.ser.parity = serial.PARITY_NONE #set parity check: no parity
        self.ser.stopbits = serial.STOPBITS_ONE #number of stop bits            #timeout block read
        self.ser.xonxoff = False     #disable software flow control
        self.ser.rtscts = False     #disable hardware (RTS/CTS) flow control
        self.ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
        self.ser.writeTimeout = 0    #timeout for write
        self.ser.timeout =0
        self.ser.open()
        
    def Serial_connect_rasp(self,comm,baud):
        self.ser_rasp.port = comm
        self.ser_rasp.baudrate =  baud
        self.ser_rasp.bytesize = serial.EIGHTBITS #number of bits per bytes
        self.ser_rasp.parity = serial.PARITY_NONE #set parity check: no parity
        self.ser_rasp.stopbits = serial.STOPBITS_ONE #number of stop bits            #timeout block read
        self.ser_rasp.xonxoff = False     #disable software flow control
        self.ser_rasp.rtscts = False     #disable hardware (RTS/CTS) flow control
        self.ser_rasp.dsrdtr = False       #disable hardware (DSR/DTR) flow control
        self.ser_rasp.timeout =0
        self.ser_rasp.open()

    def list_port(self):
        ports = serial.tools.list_ports.comports()
        self.commPort =([comport.device for comport in serial.tools.list_ports.comports()])
        self.numConnection = len(self.commPort)
        if  self.numConnection == 0 :
            pass
        elif self.numConnection == 1 :
            self.port_raspberry.addItem(str(self.commPort[0]))
            self.port_arduino.addItem(str(self.commPort[0]))
        else:
            self.port_raspberry.addItem(str(self.commPort[0]))
            self.port_raspberry.addItem(str(self.commPort[1]))
            self.port_arduino.addItem(str(self.commPort[0]))
            self.port_arduino.addItem(str(self.commPort[1]))

    def connect_rasp_clicked(self):
        comport = self.port_raspberry.currentText()
        baurate = self.baud_raspberry.currentText()  
        UIFunctions.Serial_connect_rasp(self,comport,baurate)
        if self.ser_rasp.isOpen():
            self.check_rasp.setChecked(True)
            self.label_7.setText('Connected')
            self.btnconnect_rasp.setStyleSheet('QPushButton {background-color:#1eff1e; color: white;}') 
            self.btn_disconnect_rasp.setStyleSheet('QPushButton {background-color:#1b1d23; color: white;}') 
            print("connected Rasp")
                
    def connect_arduino_clicked(self):
        comport = self.port_arduino.currentText()
        baurate = self.baud_arduino.currentText()
        self.mode_check.setChecked(False)
        self.btnstart_simu.setEnabled(False)
        self.mode_check.setEnabled(False)
        UIFunctions.Serial_connect(self,comport,baurate)
        
        if self.ser.isOpen():
            self.check_arduino.setChecked(True)
            self.label_5.setText('Connected')
            if self.mode_check.isChecked() == False:
                self.start_worker_2()
                time.sleep(0.1)
                self.start_worker_read()
            x = -11.8
            y = 0.0
            z = 13.1
            yaw=0; pitch =0 ;roll = 0
            self.xposvalue.setText(str(x))
            self.yposvalue.setText(str(y))
            self.zposvalue.setText(str(z))
            self.btnconnect_arduino.setStyleSheet('QPushButton {background-color:#1eff1e; color: white;}') 
            self.btn_disconnect_arduino.setStyleSheet('QPushButton {background-color:#1b1d23; color: white;}') 
            print("connected Arduino")
                        
    def disconnect_arduino_clicked(self):
            self.ser.close()
            if not self.ser.isOpen():
                self.mode_check.setEnabled(True)
                self.btnconnect_arduino.setStyleSheet('QPushButton {background-color:#1b1d23; color: white;}') 
                self.btn_disconnect_arduino.setStyleSheet('QPushButton {background-color:#ff1e00; color: white;}')
                self.check_arduino.setChecked(False)
                self.label_5.setText('Disconnected')
                print("disconnected")
                self.xposvalue.clear()
                self.yposvalue.clear()
                self.zposvalue.clear()
                self.valuethe1.clear()
                self.valuethe2.clear()
                self.valuethe3.clear()
                self.valuethe4.clear()
                self.valuethe5.clear()
                self.valuethe6.clear()
                self.port_arduino.setCurrentIndex(0)
            
    def disconnect_rasp_clicked(self):
            self.ser_rasp.close()
            if not self.ser_rasp.isOpen():
                self.btnconnect_rasp.setStyleSheet('QPushButton {background-color:#1b1d23; color: white;}') 
                self.btn_disconnect_rasp.setStyleSheet('QPushButton {background-color:#ff1e00; color: white;}')
                self.check_rasp.setChecked(False)
                self.label_7.setText('Disconnected')
                print("disconnected Rasp")
                self.port_raspberry.setCurrentIndex(0)
                self.rasp_xpos.clear()
                self.rasp_ypos.clear()
                self.rasp_zpos.clear()
                
    def valuechange(self):
        txt = str(self.time_respond.value())
        self.time_change.setText(txt+'s')
        self.time_change.adjustSize()
        
    def get_wrist_center(gripper_point, R0g, dg = 6.5):
      xu, yu, zu = gripper_point 
        
      nx, ny, nz = R0g[0, 2], R0g[1, 2], R0g[2, 2]
      xw = xu - dg * nx
      yw = yu - dg * ny
      zw = zu - dg * nz 
    
      return np.array([xw, yw, zw])
  
    def inverse_kinematic(Px,Py,Pz,yaw,pitch,roll):
        try:
            np.cosd = lambda x : np.cos( np.deg2rad(x) )
            np.sind = lambda x : np.sin( np.deg2rad(x) )
            d0 = 14.5 
            d1 = 2.87
            d2 = 25.5
            d3 = 1.8
            d4 = 7.2
            d5 = 17.7
            d6=  0
            d7= 6.5
            Pz = Pz + d6;
            R0u = np.matrix([[1.0*np.cosd(yaw)*np.cosd(pitch), -1.0*np.sind(yaw)*np.cosd(roll) + np.sind(pitch)*np.sind(roll)*np.cosd(yaw), 1.0*np.sind(yaw)*np.sind(roll) + np.sind(pitch)*np.cosd(yaw)*np.cosd(roll)],
                             [1.0*np.sind(yaw)*np.cosd(pitch),  np.sind(yaw)*np.sind(pitch)*np.sind(roll) + 1.0*np.cosd(yaw)*np.cosd(roll), np.sind(yaw)*np.sind(pitch)*np.cosd(roll) - 1.0*np.sind(roll)*np.cosd(yaw)],
                             [          -1.0*np.sind(pitch),                                     1.0*np.sind(roll)*np.cosd(pitch),                                    1.0*np.cosd(pitch)*np.cosd(roll)]])
            rot_mat_06 = np.matrix([[-1.0, 0.0, 0.0],
                                    [0.0, 1.0, 0.0],
                                    [1.0, 0.0, -1.0]])
            r0g = R0u*rot_mat_06
            r11 = r0g[0,0] ; r12= r0g[0,1] ; r13 = r0g[0,2];
            r21 = r0g[1,0] ; r22= r0g[1,1] ; r23 = r0g[1,2];     
            r31 = r0g[2,0] ; r32= r0g[2,1] ; r33 = r0g[2,2];
            r41=0 ; r42=0 ;r43=0 ; r44=1;
            gripper_point = Px,Py,Pz
            wrist_center = UIFunctions.get_wrist_center(gripper_point, r0g, dg = d7)
            T1 =np.empty(10, dtype=object)
            T2 =np.empty(10, dtype=object)
            T3 =np.empty(10, dtype=object)
            T4 =np.empty(10, dtype=object)
            T5 =np.empty(10, dtype=object)
            T6 =np.empty(10, dtype=object)
            T1[0] = m.atan2(-wrist_center[1],-wrist_center[0])
            a3 = 2*d2*d3
            b3 = -2*(d4+d5)*d2
            c3 = wrist_center[0]*wrist_center[0] + wrist_center[1]*wrist_center[1] + wrist_center[2]*wrist_center[2] + d1*d1 + 2*wrist_center[0]*m.cos(T1[0])*d1 + 2*wrist_center[1]*m.sin(T1[0])*d1 - d2*d2 - d3*d3 -(d4+d5)*(d4+d5)
            m1 = m.sqrt(a3*a3+b3*b3-c3*c3)
            T3[0]= m.atan2(b3,a3) + m.atan2(m1,c3)
            the1 = np.rad2deg(T1[0])
            the3 = np.rad2deg(T3[0])
            
            a= d2 -(d4+d5)*np.sind(the3) + d3*np.cosd(the3)
            b = d3*np.sind(the3) + (d4+d5)*np.cosd(the3)
            c = np.cosd(the1)*wrist_center[0] + np.sind(the1)*wrist_center[1] + d1
            d = wrist_center[2];
            T2[0]= m.atan2(a*d-b*c,a*c+b*d);
            the2 = np.rad2deg(T2[0]);
            
            T_03 = np.matrix([[np.cosd(the2 + the3)*np.cosd(the1)  ,   -np.sind(the2 + the3)*np.cosd(the1) ,    np.sind(the1)   ,  -np.cosd(the1)*(d1 - d2*np.cosd(the2))],
                           [np.cosd(the2 + the3)*np.sind(the1)  ,   -np.sind(the2 + the3)*np.sind(the1) ,   -np.cosd(the1)   ,  -np.sind(the1)*(d1 - d2*np.cosd(the2))],
                           [np.sind(the2 + the3)              ,    np.cosd(the2 + the3)             ,  0               ,       d2*np.sind(the2)               ],
                           [                0               ,                0                  ,  0               ,                   1]])
            T_03_inv =np.linalg.inv(T_03)
            
            
            a5= T_03_inv[1,0]*r13+T_03_inv[1,1]*r23+T_03_inv[1,2]*r33+T_03_inv[1,3]*r43;
            T5[0]=m.atan2(m.sqrt(1-a5*a5),a5)
            the5 = np.rad2deg(T5[0])
            
            a4= (T_03_inv[2,0]*r13+T_03_inv[2,1]*r23+T_03_inv[2,2]*r33+T_03_inv[2,3]*r43)/np.sind(the5)
            b4= -(T_03_inv[0,0]*r13+T_03_inv[0,1]*r23+T_03_inv[0,2]*r33+T_03_inv[0,3]*r43)/np.sind(the5)
            T4[0]= m.atan2(a4,b4)
            the4= np.rad2deg(T4[0])
            
            T_05 =np.matrix( [[-np.cosd(the5)*(np.sind(the1)*np.sind(the4)+np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))-np.sind(the5)*(np.cosd(the1)*np.cosd(the2)*np.sind(the3)+np.cosd(the1)*np.cosd(the3)*np.sind(the2))   ,     np.sind(the5)*(np.sind(the1)*np.sind(the4)+np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))-np.cosd(the5)*(np.cosd(the1)*np.cosd(the2)*np.sind(the3)+np.cosd(the1)*np.cosd(the3)*np.sind(the2))   ,    np.cosd(the4)*np.sind(the1)-np.sind(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3))       ,   d3*np.cosd(the2 + the3)*np.cosd(the1)-np.sind(the2 + the3)*np.cosd(the1)*(d4 + d5)-d1*np.cosd(the1)+d2*np.cosd(the1)*np.cosd(the2)],
                              [np.cosd(the5)*(np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.sind(the5)*(np.cosd(the2)*np.sind(the1)*np.sind(the3)+np.cosd(the3)*np.sind(the1)*np.sind(the2))   ,     -np.sind(the5)*(np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.cosd(the5)*(np.cosd(the2)*np.sind(the1)*np.sind(the3)+np.cosd(the3)*np.sind(the1)*np.sind(the2))   ,     -np.cosd(the1)*np.cosd(the4)-np.sind(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1))    ,    d3*np.cosd(the2 + the3)*np.sind(the1)-np.sind(the2 + the3)*np.sind(the1)*(d4 + d5)-d1*np.sind(the1)+d2*np.cosd(the2)*np.sind(the1)],
                              [np.cosd(the2 + the3)*np.sind(the5)+np.sind(the2+the3)*np.cosd(the4)*np.cosd(the5) ,                                                                                                                              np.cosd(the2+the3)*np.cosd(the5)-np.sind(the2+the3)*np.cosd(the4)*np.sind(the5)   ,                                                                            np.sind(the2 + the3)*np.sind(the4)                                   ,           np.cosd(the2 + the3)*(d4 + d5) + d3*np.sind(the2 + the3)+d2*np.sind(the2)],
                              [0                                                                               ,                                                                                                          0       ,                                                                                          0        ,                                                                                                   1]])                                                                                                                                                                                                                                                                                                                   
                     
            T_05_inv = np.linalg.inv(T_05) 
            a6=T_05_inv[0,0]*r11+T_05_inv[0,1]*r21+T_05_inv[0,2]*r31+T_05_inv[0,3]*r41
            b6=-(T_05_inv[2,0]*r11+T_05_inv[2,1]*r21+T_05_inv[2,2]*r31+T_05_inv[2,3]*r41)
            T6[0]=m.atan2(b6,a6)
            the6= np.rad2deg(T6[0])
            sum2 = np.array([the1,the2,the3,
                             the4,the5,the6]) 
            return sum2
        except:
            return np.array([0,53,43,
                             0,90,0])
    
    def forward_kinemtic_draw(the):
        d0 = 14.5 
        d1 = 2.87
        d2 = 25.5
        d3 = 1.8
        d4 = 7.2
        d5 = 17.7
        d6=  0
        d7= 6.5
        the1=float(the[0])
        the2=float(the[1])
        the3=float(the[2])
        the4=float(the[3])
        the5=float(the[4])
        the6=float(the[5])
        np.cosd = lambda x : np.cos( np.deg2rad(x) )
        np.sind = lambda x : np.sin( np.deg2rad(x) )
        T_01 = np.array([[np.cosd(the1) , -np.sind(the1) , 0 , 0],
                          [np.sind(the1) ,  np.cosd(the1) , 0 , 0],
                          [0     ,      0  ,  1 , 0],
                          [0     ,      0  ,  0 , 1]])
                   
        T_02 = np.array([[ np.cosd(the1)*np.cosd(the2),  -np.cosd(the1)*np.sind(the2)  ,   np.sind(the1)  , -d1*np.cosd(the1)],
                          [np.cosd(the2)*np.sind(the1),  -np.sind(the1)*np.sind(the2)   , -np.cosd(the1)  , -d1*np.sind(the1)],
                          [np.sind(the2),              np.cosd(the2)     ,        0     ,           0],
                          [          0,                       0         ,    0        ,      1]])
                                 
        T_03 = np.array([[ np.cosd(the2 + the3)*np.cosd(the1)  ,  -np.sind(the2 + the3)*np.cosd(the1)  ,   np.sind(the1)  ,   -np.cosd(the1)*(d1 - d2*np.cosd(the2))],
                          [ np.cosd(the2 + the3)*np.sind(the1)  ,  -np.sind(the2 + the3)*np.sind(the1)  ,  -np.cosd(the1)  ,   -np.sind(the1)*(d1 - d2*np.cosd(the2))],
                          [ np.sind(the2 + the3)        ,        np.cosd(the2 + the3)   ,          0        ,              d2*np.sind(the2)],
                          [                   0         ,                      0         ,     0             ,                     1]])
        
        T_04 = np.array([[ -np.sind(the1)*np.sind(the4)-np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3) - np.cosd(the1)*np.cosd(the2)*np.cosd(the3))  ,      np.sind(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3))-np.cosd(the4)*np.sind(the1)   ,    -np.sind(the2 + the3)*np.cosd(the1)   ,     d3*np.cosd(the2 + the3)*np.cosd(the1)-np.sind(the2 + the3)*np.cosd(the1)*(d4 + d5) - d1*np.cosd(the1)+d2*np.cosd(the1)*np.cosd(the2)],
                          [np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3) - np.cosd(the2)*np.cosd(the3)*np.sind(the1))    ,     np.cosd(the1)*np.cosd(the4)+np.sind(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1))    ,   -np.sind(the2 + the3)*np.sind(the1)    ,    d3*np.cosd(the2 + the3)*np.sind(the1)-np.sind(the2 + the3)*np.sind(the1)*(d4 + d5) - d1*np.sind(the1)+d2*np.cosd(the2)*np.sind(the1)],
                          [np.sind(the2 + the3)*np.cosd(the4)                      ,                                                              -np.sind(the2 + the3)*np.sind(the4)           ,       np.cosd(the2 + the3)                               ,                      np.cosd(the2 + the3)*(d4 + d5) + d3*np.sind(the2+the3)+d2*np.sind(the2)],
                          [0                                                       ,                                                         0           ,                      0               ,                                                                                                    1]])
         
          
        T_05 = np.array([[ -np.cosd(the5)*(np.sind(the1)*np.sind(the4)+np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))-np.sind(the5)*(np.cosd(the1)*np.cosd(the2)*np.sind(the3)+np.cosd(the1)*np.cosd(the3)*np.sind(the2))    ,    np.sind(the5)*(np.sind(the1)*np.sind(the4)+np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))-np.cosd(the5)*(np.cosd(the1)*np.cosd(the2)*np.sind(the3)+np.cosd(the1)*np.cosd(the3)*np.sind(the2))   ,    np.cosd(the4)*np.sind(the1)-np.sind(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3))    ,      d3*np.cosd(the2 + the3)*np.cosd(the1)-np.sind(the2 + the3)*np.cosd(the1)*(d4 + d5)-d1*np.cosd(the1)+d2*np.cosd(the1)*np.cosd(the2)],
                          [np.cosd(the5)*(np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.sind(the5)*(np.cosd(the2)*np.sind(the1)*np.sind(the3)+np.cosd(the3)*np.sind(the1)*np.sind(the2))     ,   -np.sind(the5)*(np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.cosd(the5)*(np.cosd(the2)*np.sind(the1)*np.sind(the3)+np.cosd(the3)*np.sind(the1)*np.sind(the2))    ,    -np.cosd(the1)*np.cosd(the4)-np.sind(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1))   ,     d3*np.cosd(the2 + the3)*np.sind(the1)-np.sind(the2 + the3)*np.sind(the1)*(d4 + d5)-d1*np.sind(the1)+d2*np.cosd(the2)*np.sind(the1)],
                          [np.cosd(the2 + the3)*np.sind(the5)+np.sind(the2+the3)*np.cosd(the4)*np.cosd(the5)          ,                                                                                                                     np.cosd(the2+the3)*np.cosd(the5)-np.sind(the2+the3)*np.cosd(the4)*np.sind(the5)    ,                                                                           np.sind(the2 + the3)*np.sind(the4)              ,                                np.cosd(the2 + the3)*(d4 + d5) + d3*np.sind(the2 + the3)+d2*np.sind(the2)],
                          [0                                                                                          ,                                                                                               0            ,                                                                                     0                                      ,                                                                     1]])
                          
        T_06 = np.array([[-np.sind(the6)*(np.cosd(the4)*np.sind(the1)-np.sind(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))-np.cosd(the6)*(np.cosd(the5)*(np.sind(the1)*np.sind(the4)+np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))+np.sind(the5)*(np.cosd(the1)*np.cosd(the2)*np.sind(the3)+np.cosd(the1)*np.cosd(the3)*np.sind(the2)))  ,      np.sind(the6)*(np.cosd(the5)*(np.sind(the1)*np.sind(the4)+np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))+np.sind(the5)*(np.cosd(the1)*np.cosd(the2)*np.sind(the3)+np.cosd(the1)*np.cosd(the3)*np.sind(the2)))-np.cosd(the6)*(np.cosd(the4)*np.sind(the1)-np.sind(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))    ,    np.sind(the5)*(np.sind(the1)*np.sind(the4)+np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))-np.cosd(the5)*(np.cosd(the1)*np.cosd(the2)*np.sind(the3)+np.cosd(the1)*np.cosd(the3)*np.sind(the2))          ,       d3*np.cosd(the2 + the3)*np.cosd(the1)-np.sind(the2 + the3)*np.cosd(the1)*(d4 + d5)-d1*np.cosd(the1)+d2*np.cosd(the1)*np.cosd(the2)],
                          [np.sind(the6)*(np.cosd(the1)*np.cosd(the4)+np.sind(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))+np.cosd(the6)*(np.cosd(the5)*(np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.sind(the5)*(np.cosd(the2)*np.sind(the1)*np.sind(the3)+np.cosd(the3)*np.sind(the1)*np.sind(the2)))   ,       np.cosd(the6)*(np.cosd(the1)*np.cosd(the4)+np.sind(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.sind(the6)*(np.cosd(the5)*(np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.sind(the5)*(np.cosd(the2)*np.sind(the1)*np.sind(the3)+np.cosd(the3)*np.sind(the1)*np.sind(the2)))   ,    -np.sind(the5)*(np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.cosd(the5)*(np.cosd(the2)*np.sind(the1)*np.sind(the3)+np.cosd(the3)*np.sind(the1)*np.sind(the2))         ,       d3*np.cosd(the2 + the3)*np.sind(the1)-np.sind(the2 + the3)*np.sind(the1)*(d4 + d5)-d1*np.sind(the1)+d2*np.cosd(the2)*np.sind(the1)],
                          [np.cosd(the6)*(np.cosd(the2 + the3)*np.sind(the5)+np.sind(the2 + the3)*np.cosd(the4)*np.cosd(the5))-np.sind(the2 + the3)*np.sind(the4)*np.sind(the6)           ,                                                                                                                                                                                 -np.sind(the6)*(np.cosd(the2 + the3)*np.sind(the5)+np.sind(the2 + the3)*np.cosd(the4)*np.cosd(the5))-np.sind(the2 + the3)*np.cosd(the6)*np.sind(the4)                               ,                                                                                                               np.cosd(the2 + the3)*np.cosd(the5)-np.sind(the2 + the3)*np.cosd(the4)*np.sind(the5)                        ,                                     np.cosd(the2 + the3)*(d4 + d5)+d3*np.sind(the2 + the3)+d2*np.sind(the2)],
                          [0                                                                                          ,                                                                                               0        ,                                                                                         0        ,                                                                                                   1]])
        P1_1org = np.array([0,0,0])
        P2_2org = np.array([0,0,0])
        P3_3org = np.array([0,0,0])
        P3_ee=    np.array([d3,0,0])
        P4_4org = np.array([0,0,-d5])
        P5_5org = np.array([0,0,0])
        P6_ee = np.array([0,0,d6+d7])
        P_0_1_EX = np.dot(T_01,np.append(P1_1org,1))
        P_0_2_EX = np.dot(T_02,np.append(P2_2org,1))
        P_0_3_EX = np.dot(T_03,np.append(P3_3org,1))
        P_0_3ee  = np.dot(T_03,np.append(P3_ee,1))
        P_0_4_EX = np.dot(T_04,np.append(P4_4org,1))
        P_0_5_EX = np.dot(T_05,np.append(P5_5org,1))
        P_0_6_EX = np.dot(T_06,np.append(P6_ee,1))
        
        X=np.array([P_0_1_EX[0],P_0_2_EX[0],P_0_3_EX[0],P_0_3ee[0],P_0_4_EX[0],P_0_5_EX[0],P_0_6_EX[0]])
        Y=np.array([P_0_1_EX[1],P_0_2_EX[1],P_0_3_EX[1],P_0_3ee[1], P_0_4_EX[1],P_0_5_EX[1],P_0_6_EX[1]])
        Z=np.array([P_0_1_EX[2],P_0_2_EX[2],P_0_3_EX[2],P_0_3ee[2], P_0_4_EX[2],P_0_5_EX[2],P_0_6_EX[2]])
        return X,Y,Z
    
    def forward_kinemtic(the):
        d0 = 14.5 
        d1 = 2.87
        d2 = 25.5
        d3 = 1.8
        d4 = 7.2
        d5 = 17.7
        d6=  0
        d7= 6.5
        the1=float(the[0])
        the2=float(the[1])
        the3=float(the[2])
        the4=float(the[3])
        the5=float(the[4])
        the6=float(the[5])
        np.cosd = lambda x : np.cos( np.deg2rad(x) )
        np.sind = lambda x : np.sin( np.deg2rad(x) )
        T_01 = np.array([[np.cosd(the1) , -np.sind(the1) , 0 , 0],
                          [np.sind(the1) ,  np.cosd(the1) , 0 , 0],
                          [0     ,      0  ,  1 , 0],
                          [0     ,      0  ,  0 , 1]])
                   
        T_02 = np.array([[ np.cosd(the1)*np.cosd(the2),  -np.cosd(the1)*np.sind(the2)  ,   np.sind(the1)  , -d1*np.cosd(the1)],
                          [np.cosd(the2)*np.sind(the1),  -np.sind(the1)*np.sind(the2)   , -np.cosd(the1)  , -d1*np.sind(the1)],
                          [np.sind(the2),              np.cosd(the2)     ,        0     ,           0],
                          [          0,                       0         ,    0        ,      1]])
                                 
        T_03 = np.array([[ np.cosd(the2 + the3)*np.cosd(the1)  ,  -np.sind(the2 + the3)*np.cosd(the1)  ,   np.sind(the1)  ,   -np.cosd(the1)*(d1 - d2*np.cosd(the2))],
                          [ np.cosd(the2 + the3)*np.sind(the1)  ,  -np.sind(the2 + the3)*np.sind(the1)  ,  -np.cosd(the1)  ,   -np.sind(the1)*(d1 - d2*np.cosd(the2))],
                          [ np.sind(the2 + the3)        ,        np.cosd(the2 + the3)   ,          0        ,              d2*np.sind(the2)],
                          [                   0         ,                      0         ,     0             ,                     1]])
        
        T_04 = np.array([[ -np.sind(the1)*np.sind(the4)-np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3) - np.cosd(the1)*np.cosd(the2)*np.cosd(the3))  ,      np.sind(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3))-np.cosd(the4)*np.sind(the1)   ,    -np.sind(the2 + the3)*np.cosd(the1)   ,     d3*np.cosd(the2 + the3)*np.cosd(the1)-np.sind(the2 + the3)*np.cosd(the1)*(d4 + d5) - d1*np.cosd(the1)+d2*np.cosd(the1)*np.cosd(the2)],
                          [np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3) - np.cosd(the2)*np.cosd(the3)*np.sind(the1))    ,     np.cosd(the1)*np.cosd(the4)+np.sind(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1))    ,   -np.sind(the2 + the3)*np.sind(the1)    ,    d3*np.cosd(the2 + the3)*np.sind(the1)-np.sind(the2 + the3)*np.sind(the1)*(d4 + d5) - d1*np.sind(the1)+d2*np.cosd(the2)*np.sind(the1)],
                          [np.sind(the2 + the3)*np.cosd(the4)                      ,                                                              -np.sind(the2 + the3)*np.sind(the4)           ,       np.cosd(the2 + the3)                               ,                      np.cosd(the2 + the3)*(d4 + d5) + d3*np.sind(the2+the3)+d2*np.sind(the2)],
                          [0                                                       ,                                                         0           ,                      0               ,                                                                                                    1]])
         
          
        T_05 = np.array([[ -np.cosd(the5)*(np.sind(the1)*np.sind(the4)+np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))-np.sind(the5)*(np.cosd(the1)*np.cosd(the2)*np.sind(the3)+np.cosd(the1)*np.cosd(the3)*np.sind(the2))    ,    np.sind(the5)*(np.sind(the1)*np.sind(the4)+np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))-np.cosd(the5)*(np.cosd(the1)*np.cosd(the2)*np.sind(the3)+np.cosd(the1)*np.cosd(the3)*np.sind(the2))   ,    np.cosd(the4)*np.sind(the1)-np.sind(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3))    ,      d3*np.cosd(the2 + the3)*np.cosd(the1)-np.sind(the2 + the3)*np.cosd(the1)*(d4 + d5)-d1*np.cosd(the1)+d2*np.cosd(the1)*np.cosd(the2)],
                          [np.cosd(the5)*(np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.sind(the5)*(np.cosd(the2)*np.sind(the1)*np.sind(the3)+np.cosd(the3)*np.sind(the1)*np.sind(the2))     ,   -np.sind(the5)*(np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.cosd(the5)*(np.cosd(the2)*np.sind(the1)*np.sind(the3)+np.cosd(the3)*np.sind(the1)*np.sind(the2))    ,    -np.cosd(the1)*np.cosd(the4)-np.sind(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1))   ,     d3*np.cosd(the2 + the3)*np.sind(the1)-np.sind(the2 + the3)*np.sind(the1)*(d4 + d5)-d1*np.sind(the1)+d2*np.cosd(the2)*np.sind(the1)],
                          [np.cosd(the2 + the3)*np.sind(the5)+np.sind(the2+the3)*np.cosd(the4)*np.cosd(the5)          ,                                                                                                                     np.cosd(the2+the3)*np.cosd(the5)-np.sind(the2+the3)*np.cosd(the4)*np.sind(the5)    ,                                                                           np.sind(the2 + the3)*np.sind(the4)              ,                                np.cosd(the2 + the3)*(d4 + d5) + d3*np.sind(the2 + the3)+d2*np.sind(the2)],
                          [0                                                                                          ,                                                                                               0            ,                                                                                     0                                      ,                                                                     1]])
                          
        T_06 = np.array([[-np.sind(the6)*(np.cosd(the4)*np.sind(the1)-np.sind(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))-np.cosd(the6)*(np.cosd(the5)*(np.sind(the1)*np.sind(the4)+np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))+np.sind(the5)*(np.cosd(the1)*np.cosd(the2)*np.sind(the3)+np.cosd(the1)*np.cosd(the3)*np.sind(the2)))  ,      np.sind(the6)*(np.cosd(the5)*(np.sind(the1)*np.sind(the4)+np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))+np.sind(the5)*(np.cosd(the1)*np.cosd(the2)*np.sind(the3)+np.cosd(the1)*np.cosd(the3)*np.sind(the2)))-np.cosd(the6)*(np.cosd(the4)*np.sind(the1)-np.sind(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))    ,    np.sind(the5)*(np.sind(the1)*np.sind(the4)+np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))-np.cosd(the5)*(np.cosd(the1)*np.cosd(the2)*np.sind(the3)+np.cosd(the1)*np.cosd(the3)*np.sind(the2))          ,       d3*np.cosd(the2 + the3)*np.cosd(the1)-np.sind(the2 + the3)*np.cosd(the1)*(d4 + d5)-d1*np.cosd(the1)+d2*np.cosd(the1)*np.cosd(the2)],
                          [np.sind(the6)*(np.cosd(the1)*np.cosd(the4)+np.sind(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))+np.cosd(the6)*(np.cosd(the5)*(np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.sind(the5)*(np.cosd(the2)*np.sind(the1)*np.sind(the3)+np.cosd(the3)*np.sind(the1)*np.sind(the2)))   ,       np.cosd(the6)*(np.cosd(the1)*np.cosd(the4)+np.sind(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.sind(the6)*(np.cosd(the5)*(np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.sind(the5)*(np.cosd(the2)*np.sind(the1)*np.sind(the3)+np.cosd(the3)*np.sind(the1)*np.sind(the2)))   ,    -np.sind(the5)*(np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.cosd(the5)*(np.cosd(the2)*np.sind(the1)*np.sind(the3)+np.cosd(the3)*np.sind(the1)*np.sind(the2))         ,       d3*np.cosd(the2 + the3)*np.sind(the1)-np.sind(the2 + the3)*np.sind(the1)*(d4 + d5)-d1*np.sind(the1)+d2*np.cosd(the2)*np.sind(the1)],
                          [np.cosd(the6)*(np.cosd(the2 + the3)*np.sind(the5)+np.sind(the2 + the3)*np.cosd(the4)*np.cosd(the5))-np.sind(the2 + the3)*np.sind(the4)*np.sind(the6)           ,                                                                                                                                                                                 -np.sind(the6)*(np.cosd(the2 + the3)*np.sind(the5)+np.sind(the2 + the3)*np.cosd(the4)*np.cosd(the5))-np.sind(the2 + the3)*np.cosd(the6)*np.sind(the4)                               ,                                                                                                               np.cosd(the2 + the3)*np.cosd(the5)-np.sind(the2 + the3)*np.cosd(the4)*np.sind(the5)                        ,                                     np.cosd(the2 + the3)*(d4 + d5)+d3*np.sind(the2 + the3)+d2*np.sind(the2)],
                          [0                                                                                          ,                                                                                               0        ,                                                                                         0        ,                                                                                                   1]])

        p6_EE = (np.matrix([0.0,0.0,float(d6+d7),1.0])).T
        p_0_6_EX =np.dot(T_06,p6_EE)
        X = str(p_0_6_EX[0][0]).strip("[]")
        Y = str(p_0_6_EX[1][0]).strip("[]")
        Z = str(p_0_6_EX[2][0]).strip("[]")
        return float(X),float(Y),float(Z)

    def send(self,x,y,z,yaw,pitch,roll):
       self.time = self.time_respond.value()
       self.xposvalue.setText(str(x))
       self.yposvalue.setText(str(y))
       self.zposvalue.setText(str(z))
       self.yaw_value.setText(str(yaw))
       self.pitch_value.setText(str(pitch))
       self.roll_value.setText(str(roll))
       self.setthe = np.round_(UIFunctions.inverse_kinematic(x,y,z,yaw,pitch,roll),1)
       self.sum = np.array([self.setthe[0],self.setthe[1],self.setthe[2],
                               self.setthe[3],self.setthe[4],self.setthe[5],self.time])
       if(self.ser.isOpen() and self.mode_check.isChecked() == False):
            self.ser.write('{},{},{},{},{},{},{}'.format(*self.sum).encode())
            Data_send =str('{},{},{},{},{},{},{}'.format(*self.sum))
            self.ser.flushInput()  #flush input buffer, discarding all its contents
            self.ser.flushOutput()
            print(Data_send)

    def simulation_check(self):
        if self.mode_check.isChecked():
            self.btnstart_simu.setEnabled(True)
            self.check_camera_4.setChecked(True)
            self.label_8.setText('Connected')
        else:
            self.btnstart_simu.setEnabled(False)
            self.check_camera_4.setChecked(False)
            self.label_8.setText('Disconnected')

            
    def start_simulation(self):
        self.the1pre = self.the2pre = self.the3pre = self.the4pre = self.the5pre =self.the6pre =0
        self.valuethe1.setText(str(self.the1pre))
        self.valuethe2.setText(str(self.the2pre))
        self.valuethe3.setText(str(self.the3pre))
        self.valuethe4.setText(str(self.the4pre))
        self.valuethe5.setText(str(self.the5pre))
        self.valuethe6.setText(str(self.the6pre))
        x = -11.8
        y = 0.0
        z = 13.1
        yaw=0; pitch =0 ;roll = 0
        UIFunctions.send(self,x,y,z,yaw,pitch,roll)
        self.start_worker_mode()

    def forward_signal(self):
        set_x = float(self.xposvalue.text()) - 10
        #set_x = float(self.rasp_xpos.text())
        set_y = float(self.yposvalue.text())
        set_z = float(self.zposvalue.text())
        yaw   = float(self.yaw_value.text()) 
        pitch = float(self.pitch_value.text())
        roll  = float(self.roll_value.text())
        self.stop_worker_mode()
        UIFunctions.send(self,set_x,set_y,set_z,yaw,pitch,roll)
        self.start_worker_mode()
    def backward_signal(self):
        set_x = float(self.xposvalue.text()) + 10
        set_y = float(self.yposvalue.text())
        set_z = float(self.zposvalue.text())
        yaw   = float(self.yaw_value.text()) 
        pitch = float(self.pitch_value.text())
        roll  = float(self.roll_value.text())
        self.stop_worker_mode()
        UIFunctions.send(self,set_x,set_y,set_z,yaw,pitch,roll)
        self.start_worker_mode()
    def left_signal(self):
        set_x = float(self.xposvalue.text())
        set_y = float(self.yposvalue.text()) - 10
        #set_y = float(self.rasp_ypos.text())
        set_z = float(self.zposvalue.text())
        yaw   = float(self.yaw_value.text()) 
        pitch = float(self.pitch_value.text())
        roll  = float(self.roll_value.text())
        self.stop_worker_mode()
        UIFunctions.send(self,set_x,set_y,set_z,yaw,pitch,roll)
        self.start_worker_mode()
    def right_signal(self):
        set_x = float(self.xposvalue.text())
        set_y = float(self.yposvalue.text()) + 10
        set_z = float(self.zposvalue.text())
        yaw   = float(self.yaw_value.text()) 
        pitch = float(self.pitch_value.text())
        roll  = float(self.roll_value.text())
        self.stop_worker_mode()
        UIFunctions.send(self,set_x,set_y,set_z,yaw,pitch,roll)
        self.start_worker_mode()
    def up_signal(self):
        set_x = float(self.xposvalue.text())
        set_y = float(self.yposvalue.text()) 
        set_z = float(self.zposvalue.text()) + 10
        yaw   = float(self.yaw_value.text()) 
        pitch = float(self.pitch_value.text())
        roll  = float(self.roll_value.text())
        self.stop_worker_mode()
        UIFunctions.send(self,set_x,set_y,set_z,yaw,pitch,roll)
        self.start_worker_mode()
    def down_signal(self):
        set_x = float(self.xposvalue.text())
        set_y = float(self.yposvalue.text())
        set_z = float(self.zposvalue.text()) - 10
        #set_z = float(self.rasp_zpos.text())
        yaw   = float(self.yaw_value.text()) 
        pitch = float(self.pitch_value.text())
        roll  = float(self.roll_value.text())
        self.stop_worker_mode()
        UIFunctions.send(self,set_x,set_y,set_z,yaw,pitch,roll)
        self.start_worker_mode()
    def send_home(self):
        x = -11.8
        y = 0.0
        z = 13.1
        yaw   = float(self.yaw_value.text()) 
        pitch = float(self.pitch_value.text())
        roll  = float(self.roll_value.text())
        self.stop_worker_mode()
        UIFunctions.send(self,x,y,z,yaw,pitch,roll)
        self.start_worker_mode()
        
    def send_inverse(self):
        set_x = float(self.ik_x.text())
        set_y = float(self.ik_y.text())
        set_z = float(self.ik_z.text())
        yaw   = float(self.yaw_value.text()) 
        pitch = float(self.pitch_value.text())
        roll  = float(self.roll_value.text())
        self.stop_worker_mode()
        UIFunctions.send(self,set_x,set_y,set_z,yaw,pitch,roll)
        self.start_worker_mode()

    def rollupMethod(self):
        val = float(self.roll_value.text())
        if(val<180):
                val+= 20.0
                self.roll_value.setText(str(round(val,2)))
                set_x = float(self.xposvalue.text())
                set_y = float(self.yposvalue.text())
                set_z = float(self.zposvalue.text())
                yaw   = float(self.yaw_value.text()) 
                pitch = float(self.pitch_value.text())
                roll  = float(self.roll_value.text())
                self.stop_worker_mode()
                UIFunctions.send(self,set_x,set_y,set_z,yaw,pitch,roll)
                self.start_worker_mode()
    def rollDownMethod(self):
        val = float(self.roll_value.text())
        if(val>-180):
                val -= 20.0
                self.roll_value.setText(str(round(val,2)))
                
                set_x = float(self.xposvalue.text())
                set_y = float(self.yposvalue.text())
                set_z = float(self.zposvalue.text())
                yaw   = float(self.yaw_value.text()) 
                pitch = float(self.pitch_value.text())
                roll  = float(self.roll_value.text())
                self.stop_worker_mode()
                UIFunctions.send(self,set_x,set_y,set_z,yaw,pitch,roll)
                self.start_worker_mode()
    def pitchUpMethod(self):
        val = float(self.pitch_value.text())
        if(val<180):
                val+= 20.0
                self.pitch_value.setText(str(round(val,2)))
                
                set_x = float(self.xposvalue.text())
                set_y = float(self.yposvalue.text())
                set_z = float(self.zposvalue.text())
                yaw   = float(self.yaw_value.text()) 
                pitch = float(self.pitch_value.text())
                roll  = float(self.roll_value.text())
                self.stop_worker_mode()
                UIFunctions.send(self,set_x,set_y,set_z,yaw,pitch,roll)
                self.start_worker_mode()
    def pitchDownMethod(self):
        val = float(self.pitch_value.text())
        if(val>-180):
                val -= 20.0
                self.pitch_value.setText(str(round(val,2)))
                set_x = float(self.xposvalue.text())
                set_y = float(self.yposvalue.text())
                set_z = float(self.zposvalue.text())
                yaw   = float(self.yaw_value.text()) 
                pitch = float(self.pitch_value.text())
                roll  = float(self.roll_value.text())
                self.stop_worker_mode()
                UIFunctions.send(self,set_x,set_y,set_z,yaw,pitch,roll)
                self.start_worker_mode()
    def yawUpMethod(self):
        val = float(self.yaw_value.text())
        if(val<180):
                val+= 20.0
                self.yaw_value.setText(str(round(val,2)))
                
                set_x = float(self.xposvalue.text())
                set_y = float(self.yposvalue.text())
                set_z = float(self.zposvalue.text())
                yaw   = float(self.yaw_value.text()) 
                pitch = float(self.pitch_value.text())
                roll  = float(self.roll_value.text())
                self.stop_worker_mode()
                UIFunctions.send(self,set_x,set_y,set_z,yaw,pitch,roll)
                self.start_worker_mode()
    def yawDownMethod(self):
        val = float(self.yaw_value.text())
        if(val>-180):
                val -= 20.0
                self.yaw_value.setText(str(round(val,2)))
                set_x = float(self.xposvalue.text())
                set_y = float(self.yposvalue.text())
                set_z = float(self.zposvalue.text())
                yaw   = float(self.yaw_value.text()) 
                pitch = float(self.pitch_value.text())
                roll  = float(self.roll_value.text())
                self.stop_worker_mode()
                UIFunctions.send(self,set_x,set_y,set_z,yaw,pitch,roll)
                self.start_worker_mode()
    def uiDefinitions(self):
        UIFunctions.list_port(self)
        UIFunctions.read_analysis(self)
        self.widget_2.hide()
        self.time_respond.setValue(6)
        self.time_change.setText(str(self.ui.time_respond.value())+'s')
        self.ui.mode_check.setChecked(False)
        self.btnstart_simu.setEnabled(False)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        
        self.ui.widget.setGraphicsEffect(self.shadow)
        self.shadow2 = QGraphicsDropShadowEffect(self)
        self.shadow2.setBlurRadius(20)
        self.shadow2.setXOffset(0)
        self.shadow2.setYOffset(0)
        self.shadow2.setColor(QColor(0, 0, 0, 60))
        
        self.ui.frame_left_menu_3.setGraphicsEffect(self.shadow2)
        self.shadow3 = QGraphicsDropShadowEffect(self)
        self.shadow3.setBlurRadius(20)
        self.shadow3.setXOffset(0)
        self.shadow3.setYOffset(0)
        self.shadow3.setColor(QColor(0, 0, 0, 60))
        self.ui.btn_page_1.setGraphicsEffect(self.shadow3)
        
        self.shadow4 = QGraphicsDropShadowEffect(self)
        self.shadow4.setBlurRadius(20)
        self.shadow4.setXOffset(0)
        self.shadow4.setYOffset(0)
        self.shadow4.setColor(QColor(0, 0, 0, 60))
        self.ui.btn_page_2.setGraphicsEffect(self.shadow4)
        
        self.shadow5 = QGraphicsDropShadowEffect(self)
        self.shadow5.setBlurRadius(20)
        self.shadow5.setXOffset(0)
        self.shadow5.setYOffset(0)
        self.shadow5.setColor(QColor(0, 0, 0, 60))
        self.ui.btn_page_3.setGraphicsEffect(self.shadow5)
        
        self.shadow6 = QGraphicsDropShadowEffect(self)
        self.shadow6.setBlurRadius(20)
        self.shadow6.setXOffset(0)
        self.shadow6.setYOffset(0)
        self.shadow6.setColor(QColor(0, 0, 0, 60))
        self.ui.widget_2.setGraphicsEffect(self.shadow6)
        
        self.yaw_value.setText('0')
        self.pitch_value.setText('90')
        self.roll_value.setText('0')
        self.check_camera_4.setEnabled(False)
        self.check_arduino.setEnabled(False)
        self.check_rasp.setEnabled(False)
        self.check_camera.setEnabled(False)
        self.auto = False
        self.manual = False