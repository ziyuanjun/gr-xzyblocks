#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from gnuradio import gr

# for i in range (1,20):
#     arr = np.loadtxt("../build/specData"+str(i)+".txt")
#     plt.plot(np.abs(arr[:,1])/1000000.0,
#              20*np.log10(np.abs(arr[:,0])))

# #plt.show()

plt.figure()
data=np.zeros((17*512,2,10))

scanNum=0
for i in range (1,17*10+1):
    arr = np.loadtxt("../build/specData"+str(i)+".txt")
    ind=(i-1)%17
    data[ind*512:ind*512+512,:,scanNum]=arr
    if ind==16:
        scanNum+=1
        plt.plot(np.abs(data[:,1])/1000000.0,
                 20*np.log10(np.abs(data[:,0])))                 
        
plt.figure()
meanData=np.mean(data,axis=2)
plt.plot(np.abs(data[:,1,0])/1000000.0,
        20*np.log10(np.abs(meanData[:,0])))

plt.show()
