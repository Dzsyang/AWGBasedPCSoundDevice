# -- coding: utf-8 --
# @Time : 5/31/2023 3:28 PM
# @Author : Dzsyang
# @Email : linzixiang@sjtu.edu.cn
# @Software: PyCharm
import numpy as np
import wave
import struct
import matplotlib.pyplot as plt


# Set the parameters
frequency = 200
num_samples = 48000
sampling_rate = 48000.0
amplitude = 16000
file = "sine_wave.wav"


# Function of sine_wave
sine_wave = [np.sin(2 * np.pi * frequency * x/sampling_rate) for x in range(num_samples)]


# Transform to .wav file
nframes = num_samples
comptype = "NONE"
compname = "not compressed"
nchannels = 1
sampwidth = 2
wav_file = wave.open(file, 'w')
wav_file.setparams((nchannels, sampwidth, int(sampling_rate), nframes, comptype, compname))
for s in sine_wave:
    wav_file.writeframes(struct.pack('h', int(s * amplitude)))


# Check the wave
wav_file = wave.open(file, 'r')
data = wav_file.readframes(num_samples)
wav_file.close()
data = struct.unpack('{n}h'.format(n=num_samples), data)
data = np.array(data)


# Draw the wave figure
plt.plot(data[:300])
plt.title("Wave")
plt.show()
