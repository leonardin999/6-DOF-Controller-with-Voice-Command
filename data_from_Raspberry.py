# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 14:21:01 2021

@author: Leonard
"""
import serial.tools.list_ports
import serial
import time
import numpy as np
import scipy
from scipy.io import loadmat,savemat
ser_rasp =  serial.Serial(
    port='COM13',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    xonxoff = False,     #disable software flow control
    rtscts = False ,    #disable hardware (RTS/CTS) flow control
    dsrdtr = False,       #disable hardware (DSR/DTR) flow control
    timeout=0
)
ser_rasp.isOpen()

while ser_rasp.isOpen():
    try:
        strdata = ser_rasp.readline().decode()
        time.sleep(0.1)
        position = strdata.split(',')
        if len(position) == 6:
            square_position = np.array([float(position[0]),float(position[1]),5.0])
            print(square_position)
        #savemat('position.mat', mdict={'pos':data})
    except Exception as e:
        print(e)
