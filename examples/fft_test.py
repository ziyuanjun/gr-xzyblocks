#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 22:28:06 2017

@author: ziyuan
"""

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.mlab import psd
from scipy.signal import decimate

f_line = 123.456
f_demod = 122

f_sample = 1000
t_total = 100
t_win = 10
ratio = 10

t = np.arange(0, t_total, 1 / f_sample) 
x = np.sin(2*np.pi*f_line * t) + np.random.randn(len(t)) # sine plus white noise
lo = 2**.5 * np.exp(-2j*np.pi*f_demod * t) # local oscillator
y = decimate(x * lo, ratio) # demodulate and decimate to 100 Hz
z = decimate(y, ratio) # decimate further to 10 Hz

nfft = int(round(f_sample * t_win))
X, fx = psd(x, NFFT = nfft, noverlap = nfft/2, Fs = f_sample)

nfft = int(round(f_sample * t_win / ratio))
Y, fy = psd(y, NFFT = nfft, noverlap = nfft/2, Fs = f_sample / ratio)

nfft = int(round(f_sample * t_win / ratio**2))
Z, fz = psd(z, NFFT = nfft, noverlap = nfft/2, Fs = f_sample / ratio**2)
Z, fz = psd(z, NFFT = len(z), noverlap = nfft/2, Fs = f_sample / ratio**2)
plt.semilogy(fx, X, fy + f_demod, Y, fz + f_demod, Z)
plt.xlabel('Frequency (Hz)')
plt.ylabel('PSD (V^2/Hz)')
plt.legend(('Full bandwidth FFT', '100 Hz FFT', '10 Hz FFT'))
plt.show()
