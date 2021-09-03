# -*- coding: utf-8 -*-
"""
Created on Sat May 29 09:32:27 2021

@author: Leonard
"""

import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import glob
import pathlib
from IPython import display
from scipy.io import loadmat,savemat
import pandas as pd
from scipy import sparse

def sigmoid(x,Lambda):
        return 1/(1+np.exp(np.multiply(-Lambda,x)))
    
def convert_labels(y, C):
    Y = sparse.coo_matrix((np.ones_like(y),
        (y, np.arange(len(y)))), shape = (C, len(y))).toarray()
    return Y

def softmax_stable(Z):
    e_Z=Z
    A=e_Z/e_Z.sum(axis=0)
    return A

def LGU_network(xi,w,Lambda):
    ## network Function:
    net = np.dot(w.T,xi) 
    ## Activation Function for Logsig:       
    ah =sigmoid(net,Lambda)
    ## Softmax Function: 
    result = softmax_stable(ah)
    return net,ah,result


def model_load(path,keywork = 'w'):
    w = loadmat(path)   
    weight = w[keywork]
    return weight

## data from the wav file :
data_dir_mother = pathlib.Path('mini_speech_commands_Auto_Update')
if not data_dir_mother.exists():
    print('direction not found!')
commands = np.array(os.listdir(str(data_dir_mother)))
## data from the wav file after processing :
data_dir = pathlib.Path('input_Auto_Update')
if not data_dir.exists():
    print('direction not found!')
filenames = glob.glob(str(data_dir)+'/*')    
listname = os.listdir(data_dir) # dir is your directory path
data  = loadmat(filenames[0])
label = loadmat(filenames[1])
mfcc = data['mfcc']
auto_label = label['label']

index1 = [i for i, name in enumerate(auto_label) if name.strip() == commands[0]]
index2 = [i for i, name in enumerate(auto_label) if name.strip() == commands[1]]
index3 = [i for i, name in enumerate(auto_label) if name.strip() == commands[2]]
index4 = [i for i, name in enumerate(auto_label) if name.strip() == commands[3]]
index5 = [i for i, name in enumerate(auto_label) if name.strip() == commands[4]]
index6 = [i for i, name in enumerate(auto_label) if name.strip() == commands[5]]
index7 = [i for i, name in enumerate(auto_label) if name.strip() == commands[6]]
# index8 = [i for i, name in enumerate(auto_label) if name.strip() == commands[7]]
# index9 = [i for i, name in enumerate(auto_label) if name.strip() == commands[8]]
# index10 =[i for i, name in enumerate(auto_label) if name.strip() == commands[9]]
# index11 =[i for i, name in enumerate(auto_label) if name.strip() == commands[10]]
# index12 =[i for i, name in enumerate(auto_label) if name.strip() == commands[11]]

input1 = mfcc[index1,:]
input2 = mfcc[index2,:]
input3 = mfcc[index3,:]
input4 = mfcc[index4,:]
input5 = mfcc[index5,:]
input6 = mfcc[index6,:]
input7 = mfcc[index7,:]
# input8 = mfcc[index8,:]
# input9 = mfcc[index9,:]
# input10 = mfcc[index10,:]
# input11 = mfcc[index11,:]
# input12 = mfcc[index12,:]

Class = len(commands)
# initialize FeedForward For Neural Network:
nuy_w = 0.001 
nuy_lam = 5
E = 1
E_store = E
E_stop = 0.0001 # stopping criteria
epod_max = 17000 #Maximun number of Training round
epod = 0 #start Epod
## initialize the Input Layer:
original_label = np.asarray([0]*len(input1) + [1]*len(input2)+ [2]*len(input3)+ [3]*len(input4)+ [4]*len(input5)+[5]*len(input6)+ 
                             [6]*len(input7)).T#+ [7]*len(input8)+ [8]*len(input9)+ [9]*len(input10)).T# [11]*len(input12)).T
x = np.concatenate((input1,input2,input3,input4,input5,input6,input7), axis = 0).T #input6,input7,input8,input9,input10,input11,input12), axis = 0).T
x = np.concatenate((x,np.ones((1,len(mfcc)))), axis = 0)

## Initialize the Labels 
w =0.1*np.ones((x.shape[0],Class),order='C')
Lambda= 12*np.ones((Class,1),order='C')
lam_store = Lambda
# w =  w_init
d = x.shape[0]
C = w.shape[1]
y = convert_labels(original_label,Class)

dE_dlam = np.zeros(Class)
dE_dw = np.zeros(Class)
dE_dw = dE_dw.tolist()
dE_dlam = dE_dlam.tolist()
while (E>E_stop) and (epod<epod_max): ## initialize the Stopping Condition
  epod = epod + 1
  print(epod)
  E = 0       
  for i in range(x.shape[1]):
    xi = x[:,i].reshape(d,1)
    yi = y[:,i].reshape(C,1)
    [net,ah,s]= LGU_network(xi,w,Lambda)
    #sai so
    e = s - yi            
    ## Back-Propagation
    #dE_de = e, de_da =1 ,  dE_dw = sum(dE_de*de_da*da_dah)*(dah_dnet*dnet_dw)       
    da_dah_s   =  (sum(ah)-ah)/(sum(ah))**2
    da_dah     = -(ah)/(sum(ah))**2 
    dnet_dw = xi.T
    dah_dnet = (np.multiply(Lambda,np.exp(np.multiply(-Lambda,net)))/(1 + np.exp(np.multiply(-Lambda,net)))**2)
    dah_dlam = (np.multiply(net,np.exp(np.multiply(-Lambda,net)))/(1 + np.exp(np.multiply(-Lambda,net)))**2)
    for j in range(len(dE_dw)):
        dE_dw[j] =0
        for l in range(len(dE_dw)):
            if(j==l):
                dE_dw[j] += (e[l]*da_dah_s[l])*(dah_dnet[j]*dnet_dw)
                dE_dlam[j] +=(e[l]*da_dah_s[l])
            else:
                dE_dw[j] += (e[l]*da_dah[l])*(dah_dnet[j]*dnet_dw)
                dE_dlam[j] +=(e[l]*da_dah[l])
        dE_dlam[j] = dE_dlam[j]*dah_dlam[j]    
    dE_dw = np.asarray(dE_dw).reshape(Class,1,18)
    dE_dlam = np.asarray(dE_dlam).reshape(Class,1)
    
    for k in range (len(Lambda)):
        Lambda[k] = (1-0.001*(np.dot(e.T,e))/(np.dot(e.T,e)+1 ))*Lambda[k] - nuy_lam*dE_dlam[k]
        w[:,k] = w[:,k] - nuy_w*dE_dw[k]
    
    E = E + 0.5*((e[0])**2 + (e[1])**2 + (e[2])**2 +(e[3])**2 + (e[4])**2 +  
                 (e[5])**2 + (e[6])**2 )
  E_store =np.append(E_store,E)
  lam_store =np.append(lam_store,Lambda)
fig = plt.figure(figsize=(15,10))
plt.plot(E_store)
plt.grid(True) 
fig = plt.figure(figsize=(15,10))
plt.plot(lam_store)
plt.grid(True) 
savemat('coeffs_Auto_Update\weight.mat', mdict={'w': w})
savemat('coeffs_Auto_Update\Lambda.mat', mdict={'lambda': Lambda})
