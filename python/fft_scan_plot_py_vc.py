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
from gnuradio import gr
from scipy import signal
import sys,time

class fft_scan_plot_py_vc(gr.sync_block):
    """
    docstring for block fft_scan_plot_py_vc
    """

    plotData=np.zeros(1024)
    xaxisData=np.linspace(30,100,1024)
    def __init__(self, device, sampRate=2.5e6, Nfft=1024, freqCenter=30e6,
                 freqMin=30e6, freqMax=2e9, protectNum=15, spectOverlapPNum=0,
                 window=None,alpha=1):
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
        self.Ne=Nfft-self.spectDropPNum*2
        fft_scan_plot_py_vc.plotData=np.zeros(int(N*self.Ne),dtype=complex)
        fft_scan_plot_py_vc.xaxisData=np.linspace(freqMin-sampRate/Nfft*self.Ne/2,
                                                  self.freqSetList[-1]+sampRate/Nfft*self.Ne/2,
                                                  int(N*self.Ne))
        self.alpha=alpha


    def work(self, input_items, output_items):
        in0 = input_items[0]

        if(self.numAfterSet==self.protectNum):
            X=fftshift(fft(in0[0]*self.window))/self.Nfft
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

    def set_alpha(self,alpha):
        self.alpha=alpha

    def set_freq_via_list(self):
        # change the freqCenter of device
        Nfreq=len(self.freqSetList)
        self.freqSetInd=self.freqSetInd+1
        if(self.freqSetInd>=Nfreq):
            self.freqSetInd=0
            self.numFrameGet+=1
            header=str(self.numFrameGet)
            sys.stdout.write('\r')
            sys.stdout.write(' ' * (Nfreq+len(header)+1) +'|\r')
            sys.stdout.write(header+'|')
            sys.stdout.flush()
        self.freqCenter=self.freqSetList[self.freqSetInd]
        self.device.set_center_freq(self.freqCenter, 0)
        sys.stdout.write('#')
        sys.stdout.flush()

