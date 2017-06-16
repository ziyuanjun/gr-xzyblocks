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
import pandas as pd
from numpy.fft import fft, fftshift
from gnuradio import gr
from scipy import signal
import sys,time
import threading

class fft_scan_plot_py_vc(gr.sync_block):
    """
    docstring for block fft_scan_plot_py_vc
    """

    def __init__(self, device, sampRate=2.5e6, Nfft=1024, freqCenter=30e6,
                 freqMin=30e6, freqMax=2e9, protectNum=15, spectOverlapPNum=0,
                 window=None,alpha=1, saveFlag=False):
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
        self.lock=threading.Lock()

        gr.sync_block.__init__(self,
            name="fft_scan_sink_py_vcc",
            in_sig=[(numpy.complex64,Nfft)],
            out_sig=None)
        self.freqCenter=freqCenter
        self.freqMin=freqMin
        self.freqMax=freqMax
        self.sampRate=sampRate
        self.device=device

        self.Nfft=Nfft
        self.protectNum=protectNum #skip some inputs to let device ready
        self.spectOverlapPNum=spectOverlapPNum
        self.spectDropPNum=int(spectOverlapPNum/2)
        self.window = signal.blackman(self.Nfft)
        self.numAfterSet=0 #inputs skipping counter

        self.alpha=alpha
        self.saveFlag=saveFlag

        # update the freqlist for scanning
        self.updateFreqlist()

    def set_numSkip(self, value):
        self.lock.acquire()
        self.protectNum=value
        self.lock.release()

    def set_freqRange(self, freqMin, freqMax):
        self.freqMin=freqMin
        self.freqMax=freqMax
        self.updateFreqlist()

    def updateFreqlist(self):

        self.ratio=(self.Nfft-self.spectOverlapPNum)/self.Nfft
        if(self.ratio<=0):
            raise ArithmeticError("Wrong Overlap")
        self.deltaFreq=self.sampRate*self.ratio #the valid freq width


        self.lock.acquire()
        self.__Nfreqlist=np.int(np.ceil((self.freqMax-self.freqMin)/(self.deltaFreq)))
        self.freqSetInd=0
        self.freqSetList=[]
        self.freqSetList=[self.freqMin+n*self.deltaFreq for n in range(int(self.__Nfreqlist))]
        self.freqCenter=self.freqMin
        self.device.set_center_freq(self.freqCenter, 0)
        self.numFrameGet=0 #one frame means one total freq list has been scanned
        self.figCount=0
        self.Ne=self.Nfft-self.spectDropPNum*2 #the valid points num in one spectrum
        fft_scan_plot_py_vc.plotData=np.zeros(int(self.__Nfreqlist*self.Ne))
        fft_scan_plot_py_vc.xaxisData=np.linspace(self.freqMin-self.sampRate/self.Nfft*self.Ne/2,
                                                  self.freqSetList[-1]+
                                                  self.sampRate/self.Nfft*self.Ne/2,
                                                  int(self.__Nfreqlist*self.Ne))
        x={freq:np.zeros(self.Nfft) for freq in self.freqSetList}
        self.df = pd.DataFrame(x)
        self.fileName=time.strftime('%Y%m%d-%H%M%S',time.localtime(time.time()))+"IQ-%.2fM"%(self.sampRate/1e6)+".cvs"
        self.df.to_csv(self.fileName,index=False)
        self.IsNewfile=True
        self.lock.release()

        print self.freqMin
        print self.freqSetList

    def work(self, input_items, output_items):
        in0 = input_items[0]

        if(self.numAfterSet==self.protectNum):
            #X=fftshift(fft(in0[0]*self.window))/self.Nfft
            self.df.iloc[:,self.freqSetInd]=in0[0]
            #in0[in0==0]=1e-10 # in case airspy is not ready

            X=20*np.log10(np.abs(fftshift(fft(in0[0]*self.window))/self.Nfft))
            if self.spectOverlapPNum>0:
                if self.numFrameGet>10:
                    fft_scan_plot_py_vc.plotData[self.freqSetInd*self.Ne:
                                                (self.freqSetInd+1)*self.Ne] \
                                =(1-self.alpha)*fft_scan_plot_py_vc.plotData[self.freqSetInd*self.Ne:(self.freqSetInd+1)*self.Ne] + self.alpha*X[self.spectDropPNum:-self.spectDropPNum]
                    # fft_scan_plot_py_vc.plotData[self.freqSetInd*(self.Nfft-2*self.spectDropPNum):
                    #               (self.freqSetInd+1)*(self.Nfft-2*self.spectDropPNum)] \
                    #               =20*np.log10(np.abs(X[self.spectDropPNum:
                    #                                      -self.spectDropPNum]))
                else:
                    fft_scan_plot_py_vc.plotData[self.freqSetInd*self.Ne:
                                                (self.freqSetInd+1)*self.Ne] \
                                =X[self.spectDropPNum:-self.spectDropPNum]

            else:
                if self.numFrameGet>1:
                    fft_scan_plot_py_vc.plotData[self.freqSetInd*self.Nfft:
                                (self.freqSetInd+1)*self.Nfft] = \
                    (1-self.alpha)*fft_scan_plot_py_vc.plotData[self.freqSetInd*self.Nfft:
                                (self.freqSetInd+1)*self.Nfft] \
                    + self.alpha*X
                else:
                    fft_scan_plot_py_vc.plotData[self.freqSetInd*self.Nfft:
                                (self.freqSetInd+1)*self.Nfft] = X

            self.set_freq_via_list()
            self.numAfterSet=0
        else:
            self.numAfterSet+=1

        return len(input_items[0])

    def set_samp_rate(self, samp_rate):
        """
        change parameters after the device's samperate changed.
        """
        self.sampRate=samp_rate
        self.updateFreqlist()

    def set_alpha(self,alpha):
        self.alpha=alpha

    def set_freq_via_list(self):
        # change the freqCenter of device
        self.lock.acquire()
        self.freqSetInd=self.freqSetInd+1
        if(self.freqSetInd>=self.__Nfreqlist):
            if self.IsNewfile:
                with open(self.fileName, 'w') as f:
                    self.df.to_csv(f)
                self.IsNewfile=False
            else:
                with open(self.fileName,'a') as f:
                    self.df.to_csv(f, header=False)

            self.freqSetInd=0 #index of the current device freq in the List
            self.numFrameGet+=1
            header=str(self.numFrameGet)
            sys.stdout.write('\r')
            sys.stdout.write(' ' * (self.__Nfreqlist+len(header)+1) +'|\r')
            sys.stdout.write(header+'|')
            sys.stdout.flush()
        self.freqCenter=self.freqSetList[self.freqSetInd]
        self.device.set_center_freq(self.freqCenter, 0)

        self.lock.release()
        sys.stdout.write('#')
        sys.stdout.flush()

