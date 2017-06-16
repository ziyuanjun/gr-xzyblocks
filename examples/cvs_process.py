#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Fs=10e6
N=1024

filename="../build/20170615-105234IQ.cvs"
filename="../build/20170616-092504IQ-10.00M.cvs"
filename="../build/20170616-092510IQ-2.50M.cvs"
df=pd.read_csv(filename)
K=np.int(np.floor(len(df)/N)-1)

Fs=float(filename.split('-')[2].split('M')[0])*1e6
freq_axis=np.linspace(-Fs/2,Fs/2,N)
#num_fig=len(df.columns)
num_row=3
num_col=3

Num_freq_shift=len(df.columns)-1

print K, u"次扫描, ",Num_freq_shift,u"次移频"

for n in range(1,Num_freq_shift+1):
    faxis=(freq_axis+float(df.columns[n]))/1e6
    if((n-1)%9==0):
        plt.figure()
    plt.subplot(num_row,num_row,(n-1)%9+1)
    for i in range(K):
        data=df.iloc[1024+i*N:1024+i*N+N,n].apply(lambda x : np.complex(x))
        X=np.fft.fftshift(np.fft.fft(data.values))/N
        plt.plot(faxis,20*np.log10(np.abs(X)))
    plt.axvline(faxis[256],color='k')
    plt.axvline(faxis[N-256],color='k')
    plt.xlabel(df.columns[n])
    plt.grid(b='on')
    ax=plt.gca()
    ax.axis('tight')


plt.show()
