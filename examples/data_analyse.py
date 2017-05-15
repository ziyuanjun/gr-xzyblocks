#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from gnuradio import gr

for i in range (1,20):
    arr = np.loadtxt("../build/specData"+str(i)+".txt")
    plt.plot(np.abs(arr[:,1])/1000000.0,
             20*np.log10(np.abs(arr[:,0])))

# #plt.show()
NT=4

plt.figure()
data=np.zeros((NT*512,2,10))
X=np.zeros(NT*512)
alpha=0.1

scanNum=0
for i in range (1,NT*10+1):
    arr = np.loadtxt("../build/specData"+str(i)+".txt")
    ind=(i-1)%NT
    data[ind*512:ind*512+512,:,scanNum]=arr
    plt.clf()
    if ind==NT-1:
        plt.plot(data[:,1,scanNum]/1000000.0,
                 20*np.log10(data[:,0,scanNum]),color='k')                 

        if(scanNum==0):
            X=data[:,0,scanNum]
        else:
            X=(1-alpha)*X + alpha * data[:,0,scanNum]

        plt.plot(data[:,1,scanNum]/1000000.0,
                 20*np.log10(X),color="r",lw=2)
        plt.savefig('fig'+str(scanNum)+'.png')
        scanNum+=1

plt.figure()
meanData=np.mean(data,axis=2)
plt.plot(np.abs(data[:,1,0])/1000000.0,
        20*np.log10(np.abs(meanData[:,0])))

plt.show()
