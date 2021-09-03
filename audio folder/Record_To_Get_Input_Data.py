# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 10:47:26 2021

@author: Leonard
"""
import pyaudio
import wave
import time 
import numpy as np
import scipy.io.wavfile as wavfile
from scipy.io import wavfile
import os
from glob import glob
import numpy as np
import pandas as pd
from librosa.core import resample, to_mono
from tqdm import tqdm
import wavio
from pydub import AudioSegment
cnt = 0
def Record_module(filename = "record.wav",seconds=2):
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

def envelope(y, rate, threshold):
    mask = []
    y = pd.Series(y).apply(np.abs)
    y_mean = y.rolling(window=int(rate/20),
                       min_periods=1,
                       center=True).max()
    for mean in y_mean:
        if mean > threshold:
            mask.append(True)
        else:
            mask.append(False)
    return mask, y_mean


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
    wav = wav.astype(np.int16)
    return sr, wav


while True:
    dst_root = 'mini_speech_commands_Auto_Update/no'
    filename = 'record.wav'
    fn = 'no'
    dst_path = dst_root +'/'+ fn +str(cnt)+ ".wav"
    if os.path.exists(dst_path) is True:
        cnt+=1
    else:
        delta_time = 2
        wav,rate = Record_module(filename,delta_time)
        rate, wav = downsample_mono(filename,sr = 16000)
        mask, y_mean = envelope(wav, rate,150)
        wav = wav[mask]
        delta_sample = int(delta_time*rate)

        # cleaned audio is less than a single sample
        # pad with zeros to delta_sample size
        if wav.shape[0] < delta_sample:
            sample = np.zeros(shape=(delta_sample,), dtype=np.int16)
            sample[:wav.shape[0]] = wav
            wavfile.write(dst_path, rate, sample)
        # step through audio and save every delta_sample
        # discard the ending audio if it is too short
        else:
            trunc = wav.shape[0] % delta_sample
            for cnt, i in enumerate(np.arange(0, wav.shape[0]-trunc, delta_sample)):
                start = int(i)
                stop = int(i + delta_sample)
                sample = wav[start:stop]
                wavfile.write(dst_path, rate, sample)
        cnt+=1
        print(cnt)
        if input('Continue(Y/N)?').strip() != 'y':
            break
    