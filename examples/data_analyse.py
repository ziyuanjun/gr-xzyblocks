#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from gnuradio import gr

for i in range (1,10):
    arr = np.loadtxt("../build/specData"+str(i)+".txt")
    plt.plot(np.abs(arr[:,1])/1000000.0,
             20*np.log10(np.abs(arr[:,0])))

plt.show()
