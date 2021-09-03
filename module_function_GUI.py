# -*- coding: utf-8 -*-
"""
Created on Fri May 28 08:48:10 2021

@author: Leonard
"""

import pyaudio
import wave
import time 
import numpy as np
import scipy.io.wavfile as wavfile
from scipy.fftpack import dct
import scipy.fftpack as fft
import os
import logging
import librosa   #for audio processing
import IPython.display as ipd
import soundfile as sf
import matplotlib.pyplot as plt
import warnings
import os
import random
import glob
import pathlib
from scipy import sparse
from scipy.io import loadmat,savemat
from librosa.core import resample, to_mono
import wavio
import pandas as pd
from feature_extraction_GUI import *
warnings.filterwarnings("ignore")

################# Module Part ############################
def Record_module(filename = "record.wav",seconds=3):
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 16000  # Record at 16000 samples per second
    
    p = pyaudio.PyAudio()  # Create an interface to PortAudio
    print('Recording.....')
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)
    
    frames = []  # Initialize array to store frames
    
    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)    
    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()
    print('Finished recording')
    
    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    time.sleep(0.2)
    rate, wav = wavfile.read(filename)
    wav = wav.astype(np.int16)
    return wav,rate

########################################################### AUDIO SIGNAL PROCCESSING #################################################

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
    return mask, y_mean

def preemphasis(signal,fcut =8e3,sr = 16e3):
    """perform preemphasis on the input signal.the ideal depend on infinite impulse response low-pass filter.

    :param signal: The signal to filter.
    :param fcut: The preemphasis cut-off frequencies. 0 is no filter. defaults is 7000 Herzt
    :param sr: The sample rate Frequencies of signal. defaults is 8000 Herzt.
            alpha ={\frac  {2\pi \Delta _{T}f_{c}}{2\pi \Delta _{T}f_{c}+1}}
    :returns: the filtered signal.
    """
    Delta_T = 1/sr
    coeff = (2*np.pi*Delta_T*fcut)/((2*np.pi*Delta_T*fcut)+1)
    y = []
    y_0 = coeff*signal[0]
    y =np.append(y,y_0)
    for i in range(1,len(signal)):
        y = np.append(y,coeff*signal[i] + (1-coeff)*y[i-1])
    return y



def Window(M,dtype = None):
    """
    Return the selection window : Hamming,Haning,Blackman.

    The Hamming window is a taper formed by using a weighted cosine.

    Parameters
    ----------
    M : int
        Number of points in the output window. If zero or less, an
        empty array is returned.

    Returns
    -------
    out : ndarray
        The window, with the maximum value normalized to one (the value
        one appears only if the number of samples is odd).
    """
    if M < 1:
        return np.array([])
    if M == 1:
        return np.ones(1, float)
    else :
        n = np.arange(0, M)
        if dtype == "Hanning":
            return 0.5 - 0.5*np.cos(2.0*np.pi*n/(M-1))
        elif dtype == "Hamming":
            return 0.54 - 0.46*np.cos(2.0*np.pi*n/(M-1))
        elif dtype == "Blackman":
            return 0.42 - 0.5*np.cos(2.0*np.pi*n/(M-1))
        else:
            return np.ones((M,))
        
def framesig(sig,sr,winlen,winstep,winfunc = None):
    """Frame a signal into overlapping frames.

    :param sig: the audio signal to frame.
    :param winlen: the length of the analysis window in seconds. Default is 0.025s (25 milliseconds)
           frame_len: length of each frame measured in samples = winlen*sig
    :param winstep: the step between successive windows in seconds. Default is 0.01s (10 milliseconds)
           frame_step: number of samples after the start of the previous frame that the next frame should begin.
    :param winfunc: the analysis window to apply to each frame. By default no window is applied.
    :returns: an array of frames. Size is NUMFRAMES by frame_len.
    """
    # Convert from seconds to samples
    frame_len = winlen * sr
    frame_step   = winstep * sr  
    siglen = len(sig)
    frame_length = int(round(frame_len))
    frame_step = int(round(frame_step))
    num_frames = int(np.ceil(float(np.abs(siglen - frame_length)) / frame_step))  # Make sure that we have at least 1 frame
    
    # Pad Signal to make sure that all frames have equal number of samples without truncating any samples from the original signal
    pad_signal_length = num_frames * frame_step + frame_length
    z = np.zeros((pad_signal_length - siglen))
    pad_signal = np.append(sig, z) 
    
    indices = np.tile(np.arange(0, frame_length), (num_frames, 1)) + np.tile(np.arange(0, num_frames * frame_step, frame_step), (frame_length, 1)).T
    frames = pad_signal[indices.astype(np.int32, copy=False)]
    win = Window(frame_length,dtype=winfunc)
    return frames*win

def FFT(frames, NFFT):
    """
    Return discrete Fourier transform of real or complex sequence.

    The returned complex array contains ``y(0), y(1),..., y(n-1)``, where

    ``y(j) = (x * exp(-2*pi*sqrt(-1)*j*np.arange(n)/n)).sum()``.

    Compute the magnitude spectrum and power spectrum of each frame in frames. 
    If frames is an NxD matrix, output will be Nx(NFFT/2+1).

    :param frames: the array of frames. Each row is a frame.
    :param NFFT: the FFT length to use. If NFFT > frame_len, the frames are zero-padded.
    :returns: If frames is an NxD matrix, output will be Nx(NFFT/2+1). Each row will be the spectrum of the corresponding frame.
    """
    if np.shape(frames)[1] > NFFT:
        logging.warn(
            'frame length (%d) is greater than FFT size (%d), frame will be truncated. Increase NFFT to avoid.',
            np.shape(frames)[1], NFFT)
    complex_spec = np.fft.rfft(frames, NFFT)
    powspec = (1.0 / NFFT )*np.square(np.absolute(complex_spec))  # Power Spectrum
    return np.abs(complex_spec),powspec

def hz2mel(hz):
    """Convert a value in Hertz to Mels

    :param hz: a value in Hz. This can also be a numpy array, conversion proceeds element-wise.
    :returns: a value in Mels. If an array was passed in, an identical sized array is returned.
    """
    return 2595 * np.log10(1+hz/700.)

def mel2hz(mel):
    """Convert a value in Mels to Hertz

    :param mel: a value in Mels. This can also be a numpy array, conversion proceeds element-wise.
    :returns: a value in Hertz. If an array was passed in, an identical sized array is returned.
    """
    return 700*(10**(mel/2595.0)-1)

def get_filterbanks(nfilt=20,nfft=512,samplerate=16000,lowfreq=0,highfreq=None):
    """Compute a Mel-filterbank. The filters are stored in the rows, the columns correspond
    to fft bins. The filters are returned as an array of size nfilt * (nfft/2 + 1)

    :param nfilt: the number of filters in the filterbank, default 20.
    :param nfft: the FFT size. Default is 512.
    :param samplerate: the samplerate of the signal we are working with. Affects mel spacing.
    :param lowfreq: lowest band edge of mel filters, default 0 Hz
    :param highfreq: highest band edge of mel filters, default samplerate/2
    :returns: A numpy array of size nfilt * (nfft/2 + 1) containing filterbank. Each row holds 1 filter.
    """
    highfreq= highfreq or samplerate/2
    assert highfreq <= samplerate/2, "highfreq is greater than samplerate/2"

    # compute points evenly spaced in mels
    lowmel = hz2mel(lowfreq)
    highmel = hz2mel(highfreq)
    melpoints = np.linspace(lowmel,highmel,nfilt+2)
    # our points are in Hz, but we use fft bins, so we have to convert
    #  from Hz to fft bin number
    bin = np.floor((nfft+1)*mel2hz(melpoints)/samplerate)

    fbank = np.zeros([nfilt,nfft//2+1])
    for j in range(0,nfilt):
        for i in range(int(bin[j]), int(bin[j+1])):
            fbank[j,i] = (i - bin[j]) / (bin[j+1]-bin[j])
        for i in range(int(bin[j+1]), int(bin[j+2])):
            fbank[j,i] = (bin[j+2]-i) / (bin[j+2]-bin[j+1])
    return fbank

def area_normalization(filters,nfilt=26,samplerate=16000,lowfreq=0,highfreq=None):
    """
    we divide the triangular MEL weights by the width of the MEL band (area normalization). 
    If we wont normalize the filters, we will see the noise increase with frequency because of the filter width.
    
    Parameters
    ----------
    filters : array_like
        original Triangle Filters.
    mel_freqs : float_like
        DESCRIPTION.
    nfilt : int, optional
        The default is 26.

    Returns
    -------
    filters : array_like
        the filters after normalization.

    """
    highfreq= highfreq or samplerate/2
    assert highfreq <= samplerate/2, "highfreq is greater than samplerate/2"

    # compute points evenly spaced in mels
    lowmel = hz2mel(lowfreq)
    highmel = hz2mel(highfreq)
    melpoints = np.linspace(lowmel,highmel,nfilt+2)
    melfreqs = mel2hz(melpoints)
    enorm = 2.0 / (melfreqs[2:nfilt+2] - melfreqs[:nfilt])
    filters *= enorm[:, np.newaxis]
    return filters

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
def normalize(audio):
    audio = audio / np.max(np.abs(audio))
    return audio

def dct2(dct_filter_num, filter_len):
  basis = np.empty((dct_filter_num,filter_len))
  basis[0, :] = 1.0 / np.sqrt(filter_len)
  samples = np.arange(1, 2 * filter_len, 2) * np.pi / (2.0 * filter_len)

  for i in range(1, dct_filter_num):
      basis[i,:] = np.cos(i * samples) * np.sqrt(2.0 / filter_len)
  return basis

def mfcc(signal,samplerate=16000,winlen=0.025,winstep=0.01,numcep=13,
         nfilt=26,nfft=512,lowfreq=0,highfreq=None,fcut = 6000,ceplifter=22,open_lift = True,
         winfunc="hamming",sum_up = True,appendEnergy=True):
    """Compute MFCC features from an audio signal.

    :param signal: the audio signal from which to compute features. Should be an N*1 array
    :param samplerate: the sample rate of the signal we are working with, in Hz.
    :param winlen: the length of the analysis window in seconds. Default is 0.025s (25 milliseconds)
    :param winstep: the step between successive windows in seconds. Default is 0.01s (10 milliseconds)
    :param numcep: the number of cepstrum to return, default 13
    :param nfilt: the number of filters in the filterbank, default 26.
    :param nfft: the FFT size. Default is None, which uses the calculate_nfft function to choose the smallest size that does not drop sample data.
    :param lowfreq: lowest band edge of mel filters. In Hz, default is 0.
    :param highfreq: highest band edge of mel filters. In Hz, default is samplerate/2
    :param ceplifter: apply a lifter to final cepstral coefficients. 0 is no lifter. Default is 22.
    :param winfunc: the analysis window to apply to each frame. By default no window is applied. You can use numpy window functions here e.g. winfunc=numpy.hamming
    :returns: A numpy array of size (NUMFRAMES by numcep) containing features. Each row holds 1 feature vector.
    """
    # nfft = nfft or winlen*samplerate
    mask, env = envelope(signal,samplerate, threshold=20)
    signal = signal[mask]
    signal = preemphasis(signal,fcut,samplerate)
    frames = framesig(signal,samplerate,winlen,winstep,winfunc = "Hanning")
    [amplitudes,pspec] = FFT(frames,nfft)

    fb = get_filterbanks(nfilt,nfft,samplerate,lowfreq,highfreq)
    log_bank = np.log(fb)
    fb = area_normalization(fb,nfilt,samplerate,lowfreq,highfreq)
    dct_filters = dct2(numcep,nfilt)
    feat = np.dot(fb,pspec.T) # compute the filterbank energies
    feat = np.where(feat == 0,np.finfo(float).eps,feat) # if feat is zero, we get problems with log
    #feat = feat
    [num_coef,num_frames] = np.shape(feat)
    feat_energy = np.zeros(num_coef)
    for i in range (0,num_frames):
        feat_energy = feat_energy+feat[:,i]
    audio_log = 10*np.log10(feat_energy)
    
    cepstral_coefficents=np.dot(dct_filters,audio_log)

    cepstral_coefficents = lifter(cepstral_coefficents,ceplifter)
    cepstral_coefficents -= (np.mean(cepstral_coefficents, axis=0) + 1e-8)

    cepstral_coefficents = normalize(cepstral_coefficents)
    return cepstral_coefficents,pspec,feat,log_bank,frames

#################################################### FILE PROCESSING########################################################
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
def re_write(path):
    x,_ = librosa.load(path, sr=16000)
    sf.write(path, x,16000)


def get_wavfile_and_label():
    data_dir = pathlib.Path('mini_speech_commands')
    if not data_dir.exists():
        print('direction not found!')
    commands = np.array(os.listdir(str(data_dir)))
    commands = commands[commands != 'README.md']
    filenames = glob.glob(str(data_dir)+'/*/*')
    pathfiles = glob.glob(str(data_dir)+'/*')
    #filenames = random.shuffle(filenames)
    num_samples = len(filenames)
    print('Number of total examples:', num_samples)
    print('Number of examples per label:',
          len(os.listdir(str(data_dir/commands[0]))))
    print('Example file:', filenames[0])
    return filenames,commands
    
def get_label(file_path,filenames):
    parts=[]
    for i in range(np.size(file_path)):
        parts_take = np.array([file_path[i].split('\\')])
        parts =np.append(parts,parts_take[0,1])                                
    return parts
    label = get_label(filenames)
    rate ={}
    signal={}
    for i in range(len(filenames)):
        (rate,signal[i]) = wavfile.read(filenames[i])
    data = list(signal.values())
    return data,label
    
def mutiple_file(folder):
    mfcc_result=[]
    folder = str(folder).strip('\u202a')
    listname = os.listdir(folder) # dir is your directory path
    number_files = len(listname)
    signal={}
    mfcc={}
    for i in range(number_files):  
        Path = str(folder)+'/' + listname[i]
        (sr,signal[i]) = wavfile.read(Path.strip('\u202a'))
        mfcc_result = mfcc(signal[i],sr)
    return mfcc_result

################################################### MODEL PROCESSING #######################################
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
    ah =sigmoid(net,Lambda)
    result = softmax_stable(sum(ah))
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
    answers = label[result]
    percent = np.round(z[result],2)*100
    print('your answers is '+ answers +': {0} %'.format(percent))
    return  answers,percent

def record(Weigth,Lambda,label,filename = "record.wav",seconds=2.5):
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
