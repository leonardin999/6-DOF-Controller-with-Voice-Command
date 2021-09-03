# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 07:05:34 2020

@author: Leonard
"""

import matplotlib.pyplot as plt
import scipy.fftpack as fft
from scipy.fftpack import dct
import numpy as np
import pandas as pd
from scipy.io import wavfile
from scipy.signal import get_window
from scipy.io.wavfile import write
import warnings
from array import array
import sounddevice as sd
import time
import pyaudio
import wave
import soundfile as sf 
from librosa.core import resample, to_mono
import wavio

warnings.filterwarnings("ignore")

def stereo_to_mono(path):
    rate, wav = wavfile.read(path)
    wav = wav.astype(np.int16)
    # checks stereo and converts to mono if nessesary
    try:
        tmp = wav.shape[1]
        wav = wav[:,0]+wav[:,1] / 2
    except:
        pass
    return rate, wav

def envelope(y, rate, threshold):
    mask = []
    y = pd.Series(y).apply(np.abs)
    y_mean = y.rolling(window=int(rate/10),
                       min_periods=1,
                       center=True).max()
    for mean in y_mean:
        if mean > threshold:
            mask.append(True)
        else:
            mask.append(False)
    return mask,y_mean


def normalized_audio(audio):
    audio = audio / np.max(np.abs(audio))
    return audio

def pre_emphasized(Signals,cutting_rate,sr):
    alpha = (2*np.pi*cutting_rate)/sr
    y = []
    y1 = (alpha/(1+alpha))*Signals[0]
    y =np.append(y,y1)
    for i in range(1,len(Signals)):
        y = np.append(y,(alpha/(1+alpha))*Signals[i] + (1/(1+alpha))*y[i-1])
    return y

def pre_emphasized2(Signals,cutting_rate,sr):
    alpha = (2*np.pi*cutting_rate)/sr
    Y = (alpha/(1+alpha))*Signals[0]
    emphasized={}
    emphasized = np.append(Y,(alpha/(1+alpha))*Signals[1:] + (1/(1+alpha))*Signals[:-1])
    return np.array(emphasized)

def frame_audio(audio,frame_size,frame_stride,sample_rate):
    frame_length,frame_step=frame_size*sample_rate,frame_stride*sample_rate

    signal_length=len(audio)
    frame_length=int(round(frame_length))
    frame_step=int(round(frame_step))
    num_frames=int(np.ceil(float(np.abs(signal_length-frame_length))/frame_step))
    
    pad_signal_length=num_frames*frame_step+frame_length
    z=np.zeros((pad_signal_length-signal_length))
    pad_signal=np.append(audio,z)
    indices = np.tile(np.arange(0, frame_length), (num_frames, 1)) + np.tile(np.arange(0, num_frames * frame_step, frame_step), (frame_length, 1)).T    
    frames = pad_signal[np.mat(indices).astype(np.int16, copy=False)]
    return frames,frame_length,frame_step,num_frames

def hanning(frame_length):
    #Hann= a - b* np.cos((2 * np.pi * frame_length) / (frame_length - 1))
    Hann = get_window("hann", frame_length, fftbins=True)
    return Hann

def Fast_FT(Frames,NFFT):
    audio_winT = np.transpose(Frames)

    audio_fft = np.empty((int(NFFT), audio_winT.shape[1]), dtype=np.complex64, order='F')

    for n in range(audio_fft.shape[1]):
        audio_fft[:, n] = np.fft.fft(audio_winT[:, n], axis=0)[:audio_fft.shape[0]]
    audio_fft = abs(np.transpose(audio_fft))
    audio_power = (1.0 / NFFT)*((audio_fft) ** 2)
    return audio_power,abs(audio_fft)

def get_filter_points(fmin, fmax, mel_filter_num, NFFT, sample_rate):
    fmin_mel = 2595.0 * np.log10(1.0 + fmin / 700.0)
    fmax_mel = 2595.0 * np.log10(1.0 + fmax / 700.0)    
    mels = np.linspace(fmin_mel, fmax_mel, num=mel_filter_num+2)
    freqs = 700.0 * (10.0**(mels / 2595.0) - 1.0)
    
    return np.floor((NFFT+1) / sample_rate * freqs).astype(int), freqs

def MelFrequencyFilterBank(filter_points, NFFT):
    filters = np.zeros((len(filter_points)-2,int(NFFT)))
    
    for n in range(len(filter_points)-2):
        filters[n, filter_points[n] : filter_points[n + 1]] = np.linspace(0, 1, filter_points[n + 1] - filter_points[n])
        filters[n, filter_points[n + 1] : filter_points[n + 2]] = np.linspace(1, 0, filter_points[n + 2] - filter_points[n + 1])
    
    return filters

def dct2(dct_filter_num, filter_len):
  basis = np.empty((dct_filter_num,filter_len))
  basis[0, :] = 1.0 / np.sqrt(filter_len)
  samples = np.arange(1, 2 * filter_len, 2) * np.pi / (2.0 * filter_len)

  for i in range(1, dct_filter_num):
      basis[i,:] = np.cos(i * samples) * np.sqrt(2.0 / filter_len)
  return basis  

def lifter(cepstra, L=22):
    """Apply a cepstral lifter the the matrix of cepstra. This has the effect of increasing the
    magnitude of the high frequency DCT coeffs.

    :param cepstra: the matrix of mel-cepstra, will be numframes * numcep in size.
    :param L: the liftering coefficient to use. Default is 22. L <= 0 disables lifter.
    """
    if L > 0:
        ncoeff = len(cepstra)
        n = np.arange(ncoeff)
        lift = 1 + (L/2.)*np.sin(np.pi*n/L)
        feat = lift*cepstra
        feat -= (np.mean(feat, axis=0) + 1e-8)
        return feat
    else:
        # values of L <= 0, do nothing
        return cepstra
    
def feature_extract(audio,sr,ceplifter=22,dct_filter_num = 17):
    mask, env = envelope(audio,sr, threshold=150)
    audio = audio[mask]
    audio = normalized_audio(audio)
    Cutting_Rate = 8000
    emphasized_signal = pre_emphasized(audio,Cutting_Rate,16000)

    frame_size=0.025
    frame_stride=0.01
    [frames,frame_length,frame_step,num_frames] = frame_audio(emphasized_signal,frame_size,frame_stride,sr)
    Hann_Coeff = hanning(frame_length)
    windows = frames*Hann_Coeff   
    NFFT = 400
    [power_spectrum ,Mag] = Fast_FT(windows,NFFT)
    freq_min = 400
    freq_high = 8000
    mel_filter_num = 47
    filter_points, mel_freqs = get_filter_points(freq_min, freq_high, mel_filter_num, NFFT,sr)
    filters = MelFrequencyFilterBank(filter_points, NFFT)
    dct_filters = dct2(dct_filter_num,mel_filter_num)
    audio_filtered = np.dot(filters, np.transpose(power_spectrum))
    sum12 = np.zeros(mel_filter_num)
    for i in range (1,num_frames):
        sum12 = sum12+audio_filtered[:,i]   
    audio_log = 20*np.log10(sum12)
    
    cepstral_coefficents=np.dot(dct_filters,audio_log)
    #cepstral_coefficents=normalize_audio(cepstral_coefficents)
    cepstral_coefficents = lifter(cepstral_coefficents,ceplifter)
    cepstral_coefficents -= (np.mean(cepstral_coefficents, axis=0) + 1e-8)
    cepstral_coefficents = cepstral_coefficents/max(cepstral_coefficents)
    return cepstral_coefficents


def read_wavfile(path):
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
    wav = wav.astype(np.int16)
    return rate, wav
