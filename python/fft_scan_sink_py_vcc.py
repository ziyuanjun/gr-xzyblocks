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

from __future__ import division
import numpy
import numpy as np
from numpy.fft import fft, fftshift
import matplotlib.pyplot as plt
from gnuradio import gr
from scipy import signal

class fft_scan_sink_py_vcc(gr.sync_block):
    """
    This block can be used to get frequency specturm scanning results of given device.
    The list of devices which have been tested is: airspy.
    """
    def __init__(self, device, sampRate=2.5e6, Nfft=1024, freqCenter=30e6,
                 freqMin=30e6, freqMax=2e9, protectNum=15, spectOverlapPNum=0,
                 window=None):
        """
        device: freq scanning device
        sampRate: device real samplerate
        Nfft: number of fft points
        freqCenter: the init-center-frequency
        freqMin: the minimum frequency of scanning
        freqMax: the maximum frequency of scanning
        protectNum: now that we must wait a little after the device's freq been set,
                    we just skip several input samples(this parameter is the number)
                    in this block.
        spectOverlapPNum: specturm is not pure since the filter's edge is not sharp.
                    we must drop some FFT points. To get a continous specturm, we let
                    two adjacent FFT overlapped.
        """
        gr.sync_block.__init__(self,
            name="fft_scan_sink_py_vcc",
            in_sig=[(numpy.complex64,Nfft)],
            out_sig=None)
        self.Nfft=Nfft
        self.device=device
        self.freqCenter=freqCenter
        self.freqMin=freqMin
        self.freqMax=freqMax
        self.sampRate=sampRate
        self.figCount=0
        self.protectNum=protectNum
        self.numAfterSet=0
        self.spectOverlapPNum=spectOverlapPNum
        ratio=(Nfft-spectOverlapPNum)/Nfft
        if(ratio<=0):
            raise ArithmeticError("Wrong Overlap")
        self.deltaFreq=sampRate*ratio
        N=np.ceil((freqMax-freqMin)/(self.deltaFreq))
        self.freqSetInd=0
        self.freqSetList=[freqMin+n*self.deltaFreq for n in range(int(N))]
        print self.freqSetList
        self.spectDropPNum=int(spectOverlapPNum/2)
        self.window = signal.blackman(Nfft)
        print "win shape: ", np.shape(self.window)
        self.numFrameGet=0


    def work(self, input_items, output_items):
        in0 = input_items[0]
        # <+signal processing here+>

        if(self.numAfterSet==self.protectNum):
            #if(self.freqCenter==self.device.get_center_freq()):
            # Caculate the FFT specturm
            # if(np.shape(in0)[0]==1):
            #     return len(input_items[0])

            #print np.shape(in0), np.shape(in0[0]), 
            X=fftshift(fft(in0[0]*self.window))
            # X=fftshift(fft(((1-self.alpha)*in0[0]+self.alpha*in0[1])
            #                *self.window))

            #X=fftshift((1-self.alpha)*fft(in0[0]*self.window)+self.alpha*fft(in0[1]*self.window))
            #print "X shape: ", np.shape(X)
            freqAxis=np.linspace(self.freqCenter-self.sampRate/2,self.freqCenter+self.sampRate/2, self.Nfft)
            # plt.plot(freqAxis/1000000.0, 20*np.log10(np.abs(X)))
            # plt.savefig("specFig"+str(self.figCount)+".png")
            # plt.clf()
            # self.figCount+=1
            data=np.zeros((self.Nfft-self.spectDropPNum*2, 2),dtype=np.float)
            if self.spectOverlapPNum>0:
                data[:,0]=np.abs(X[self.spectDropPNum:-self.spectDropPNum])
                data[:,1]=freqAxis[self.spectDropPNum:-self.spectDropPNum]
            else:
                data[:,0]=np.abs(X)
                data[:,1]=freqAxis

            np.savetxt("specData"+str(self.figCount)+".txt",data)
            self.figCount+=1

            #self.set_freq()
            self.set_freq_via_list()
            self.numAfterSet=0
        else:
            self.numAfterSet+=1

        return len(input_items[0])

    def set_freq_via_list(self):
        # change the freqCenter of device
        self.freqSetInd=self.freqSetInd+1
        if(self.freqSetInd>=len(self.freqSetList)):
            self.freqSetInd=0
            self.numFrameGet+=1
            print "\n"+str(self.numFrameGet),
        self.freqCenter=self.freqSetList[self.freqSetInd]
        self.device.set_center_freq(self.freqCenter, 0)

        print "=",

    def set_freq(self):
        # change the freqCenter of device
        self.freqCenter=self.freqCenter+self.deltaFreq
        if(self.freqCenter>self.freqMax):
            self.freqCenter=self.freqMin
        elif(self.freqCenter<self.freqMin):
            self.freqCenter=self.freqMin
        self.device.set_center_freq(self.freqCenter, 0)
        print self.freqCenter/1000000.0


