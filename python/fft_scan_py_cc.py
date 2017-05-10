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
from numpy.fft import fft
import matplotlib.pyplot as plt
from gnuradio import gr

class fft_scan_py_cc(gr.basic_block):
    """
    docstring for block fft_scan_py_cc
    """
    def __init__(self, device, sampRate=2e6, Nfft=1024, freqCenter=30e6, freqMin=30e6, freqMax=2e9):
        gr.basic_block.__init__(self,
            name="fft_scan_py_cc",
            in_sig=[(numpy.complex, Nfft)],
            out_sig=[(numpy.complex, Nfft),(numpy.float32,Nfft)])
        self.Nfft=Nfft
        self.device=device
        self.freqCenter=freqCenter
        self.freqMin=freqMin
        self.freqMax=freqMax
        self.sampRate=sampRate
        self.figCount=0

    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items

    def general_work(self, input_items, output_items):
        print np.shape(output_items), np.shape(input_items)

        # Caculate the FFT specturm
        X=fft(input_items[0])
        freqAxis=np.linspace(self.freqCenter-self.sampRate/2,self.freqCenter+self.sampRate/2, self.Nfft)
        plt.plot(freqAxis, 20*np.log10(np.abs(X)))
        plt.savefig("specFig"+str(self.figCount)+".png")

        # output
        # output_items[0][:] = X
        # output_items[1][:] = freqAxis
        output_items[0][:] = input_items[0]

        # change the freqCenter of device
        self.freqCenter+=self.sampRate
        if(self.freqCenter>self.freqMax-self.sampRate):
            self.freqCenter=self.freqMin+self.sampRate
        self.device.set_center_freq(self.freqCenter, 0)

        consume(0, len(input_items[0]))
        #self.consume_each(len(input_items[0]))
        return len(output_items[0])
