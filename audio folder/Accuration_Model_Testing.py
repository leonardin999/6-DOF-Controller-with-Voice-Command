# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 08:58:56 2020

@author: Leonard
"""


import time 
import numpy as np
import glob
import pathlib
import os
from scipy import sparse
from scipy.io import loadmat
from librosa.core import resample, to_mono
import wavio
from module_function import envelope,Record_module
from feature_extraction import feature_extract
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
    print('net')
    print(net)
    ah =sigmoid(net,Lambda)
    print('ah')
    print(sum(ah))
    result = softmax_stable(sum(ah))
    print('result')
    print(result)
    return net,ah,result
def to_classlabel(z):
    return z.argmax(axis = 0),z

def downsample_mono(path, sr):
    obj = wavio.read(path)
    wav = obj.data.astype(np.float32, order='F')
    rate = obj.rate
    try:
        channel = wav.shape[1]
        if channel == 2:
            wav = to_mono(wav.T)
        elif channel == 1:
            wav = to_mono(wav.reshape(-1))
    except IndexError:
        wav = to_mono(wav.reshape(-1))
        pass
    except Exception as exc:
        raise exc
    wav = resample(wav, rate, sr)
    wav = wav.astype(np.int16)
    return sr, wav

def model_load(path,keywork = 'w'):
    w = loadmat(path)   
    weight = w[keywork]
    return weight


def evaluate(mfcc_feat,w,Lambda,label,Bias =1):
    num = len(mfcc_feat)
    mfcc_feat = mfcc_feat.reshape(num,)
    sample = np.insert(mfcc_feat,num,Bias).T
    [network,hid_sigmod,se] = LGU_network(sample,w,Lambda)
    [result,z] = to_classlabel(se)
    print(result)
    print(z)
    answers = label[result]
    percent = np.round(z[result],2)*100
    print('your answers is '+ answers +': {0} %'.format(percent))
    return  answers,percent

def record(Weigth,Lambda,label,filename = "record.wav",seconds=2):
    [record,sr]  = Record_module(filename,seconds)
    rate, wav = downsample_mono(filename,sr = 16000)
    mask, y_mean = envelope(wav, rate,160)
    wav = wav[mask]
    delta_sample = int(seconds*rate)

    if wav.shape[0] < delta_sample:
        sample = np.zeros(shape=(delta_sample,), dtype=np.int16)
        sample[:wav.shape[0]] = wav
    else:
        trunc = wav.shape[0] % delta_sample
        for cnt, i in enumerate(np.arange(0, wav.shape[0]-trunc, delta_sample)):
            start = int(i)
            stop = int(i + delta_sample)
            sample = wav[start:stop]
    time.sleep(0.1)
    samples = feature_extract(sample,sr)
    [result,percent] = evaluate(samples,Weigth,Lambda,label,Bias =1)
    return result,percent

## from the input:
data_dir = pathlib.Path('mini_speech_commands_Auto')
if not data_dir.exists():
    print('direction not found!')
label = np.array(os.listdir(str(data_dir)))
## from the model:
data_dir_model = pathlib.Path('coeffs_Auto')
if not data_dir_model.exists():
    print('direction not found!')
filenames = glob.glob(str(data_dir_model)+'/*')

while True:
    weights = model_load(filenames[1])
    Lambda = model_load(filenames[0],'lambda')
    [command,percent] = record(weights,Lambda,label) 
    print(command)
    
    if input('try Again? (Y/N)').strip().upper()!='Y':
        break          