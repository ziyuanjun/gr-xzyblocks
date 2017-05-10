#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2017 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
import numpy as np
from numpy.fft import fft, fftshift
import matplotlib.pyplot as plt
from gnuradio import gr

class fft_scan_py_vcc(gr.sync_block):
    """
    docstring for block fft_scan_py_vcc
    """
    def __init__(self, device,sampRate=2.5e6, Nfft=1024, freqCenter=30e6, freqMin=30e6, freqMax=2e9):
        gr.sync_block.__init__(self,
            name="fft_scan_py_vcc",
            in_sig=[(numpy.complex64, Nfft)],
            out_sig=[(numpy.complex64, Nfft),(numpy.float32, Nfft)])
        self.Nfft=Nfft
        self.device=device
        self.freqCenter=freqCenter
        self.freqMin=freqMin
        self.freqMax=freqMax
        self.sampRate=sampRate
        self.figCount=0
        self.protectNum=15
        self.numAfterSet=0


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        out1 = output_items[1]
        # <+signal processing here+>
        # print np.shape(input_items), np.shape(output_items)
        #print np.shape(in0), np.shape(out), self.freqCenter/1000000.0

        if(self.numAfterSet==self.protectNum):
            #if(self.freqCenter==self.device.get_center_freq()):
            # Caculate the FFT specturm
            X=fftshift(fft(in0[0]))
            #print "X shape: ", np.shape(X)
            freqAxis=np.linspace(self.freqCenter-self.sampRate/2,self.freqCenter+self.sampRate/2, self.Nfft)
            plt.plot(freqAxis/1000000.0, 20*np.log10(np.abs(X)))
            plt.savefig("specFig"+str(self.figCount)+".png")
            plt.clf()
            self.figCount+=1

            out[0][:] = X
            out1[0][:] = freqAxis

            # change the freqCenter of device
            self.freqCenter=self.freqCenter+self.sampRate
            if(self.freqCenter>self.freqMax):
                self.freqCenter=self.freqMin
            elif(self.freqCenter<self.freqMin):
                self.freqCenter=self.freqMin
            self.device.set_center_freq(self.freqCenter, 0)
            self.numAfterSet=0
        else:
            self.numAfterSet+=1

        return len(output_items[0])

