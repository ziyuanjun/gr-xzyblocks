#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Airspy Fm
# Generated: Tue Jun 27 16:20:51 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import audio
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import time
import wx


class airspy_FM(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Airspy Fm")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.freq_slider = freq_slider = 94.6e6
        self.RFgain_slider = RFgain_slider = 10
        self.IFgain_slider = IFgain_slider = 20
        self.BBgain_slider = BBgain_slider = 20
        self.samp_rate = samp_rate = 2500000
        self.freq = freq = freq_slider
        self.RF_gain = RF_gain = RFgain_slider
        self.IF_gain = IF_gain = IFgain_slider
        self.BB_gain = BB_gain = BBgain_slider

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=freq,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=55,
        	average=False,
        	avg_alpha=None,
        	title='FFT Plot',
        	peak_hold=False,
        	win=window.blackmanharris,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=2205,
                decimation=50000,
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_source_1 = osmosdr.source( args="numchan=" + str(1) + " " + 'airspy' )
        self.osmosdr_source_1.set_sample_rate(samp_rate)
        self.osmosdr_source_1.set_center_freq(freq, 0)
        self.osmosdr_source_1.set_freq_corr(0, 0)
        self.osmosdr_source_1.set_dc_offset_mode(0, 0)
        self.osmosdr_source_1.set_iq_balance_mode(0, 0)
        self.osmosdr_source_1.set_gain_mode(False, 0)
        self.osmosdr_source_1.set_gain(RF_gain, 0)
        self.osmosdr_source_1.set_if_gain(IF_gain, 0)
        self.osmosdr_source_1.set_bb_gain(BB_gain, 0)
        self.osmosdr_source_1.set_antenna('', 0)
        self.osmosdr_source_1.set_bandwidth(0, 0)

        self.low_pass_filter_0 = filter.fir_filter_ccf(4, firdes.low_pass(
        	1, samp_rate, 50000, 1000000, firdes.WIN_HAMMING, 6.76))
        _freq_slider_sizer = wx.BoxSizer(wx.VERTICAL)
        self._freq_slider_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_freq_slider_sizer,
        	value=self.freq_slider,
        	callback=self.set_freq_slider,
        	label='freq',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._freq_slider_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_freq_slider_sizer,
        	value=self.freq_slider,
        	callback=self.set_freq_slider,
        	minimum=80e6,
        	maximum=110e6,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_freq_slider_sizer)
        self.audio_sink_0 = audio.sink(22050, '', True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=500000,
        	audio_decimation=1,
        )
        _RFgain_slider_sizer = wx.BoxSizer(wx.VERTICAL)
        self._RFgain_slider_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_RFgain_slider_sizer,
        	value=self.RFgain_slider,
        	callback=self.set_RFgain_slider,
        	label='RF_gain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._RFgain_slider_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_RFgain_slider_sizer,
        	value=self.RFgain_slider,
        	callback=self.set_RFgain_slider,
        	minimum=0,
        	maximum=30,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_RFgain_slider_sizer)
        _IFgain_slider_sizer = wx.BoxSizer(wx.VERTICAL)
        self._IFgain_slider_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_IFgain_slider_sizer,
        	value=self.IFgain_slider,
        	callback=self.set_IFgain_slider,
        	label='IF_gain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._IFgain_slider_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_IFgain_slider_sizer,
        	value=self.IFgain_slider,
        	callback=self.set_IFgain_slider,
        	minimum=0,
        	maximum=30,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_IFgain_slider_sizer)
        _BBgain_slider_sizer = wx.BoxSizer(wx.VERTICAL)
        self._BBgain_slider_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_BBgain_slider_sizer,
        	value=self.BBgain_slider,
        	callback=self.set_BBgain_slider,
        	label='BB_gain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._BBgain_slider_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_BBgain_slider_sizer,
        	value=self.BBgain_slider,
        	callback=self.set_BBgain_slider,
        	minimum=0,
        	maximum=30,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_BBgain_slider_sizer)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv_0, 0))
        self.connect((self.osmosdr_source_1, 0), (self.low_pass_filter_0, 0))
        self.connect((self.osmosdr_source_1, 0), (self.wxgui_fftsink2_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.audio_sink_0, 0))

    def get_freq_slider(self):
        return self.freq_slider

    def set_freq_slider(self, freq_slider):
        self.freq_slider = freq_slider
        self.set_freq(self.freq_slider)
        self._freq_slider_slider.set_value(self.freq_slider)
        self._freq_slider_text_box.set_value(self.freq_slider)

    def get_RFgain_slider(self):
        return self.RFgain_slider

    def set_RFgain_slider(self, RFgain_slider):
        self.RFgain_slider = RFgain_slider
        self.set_RF_gain(self.RFgain_slider)
        self._RFgain_slider_slider.set_value(self.RFgain_slider)
        self._RFgain_slider_text_box.set_value(self.RFgain_slider)

    def get_IFgain_slider(self):
        return self.IFgain_slider

    def set_IFgain_slider(self, IFgain_slider):
        self.IFgain_slider = IFgain_slider
        self.set_IF_gain(self.IFgain_slider)
        self._IFgain_slider_slider.set_value(self.IFgain_slider)
        self._IFgain_slider_text_box.set_value(self.IFgain_slider)

    def get_BBgain_slider(self):
        return self.BBgain_slider

    def set_BBgain_slider(self, BBgain_slider):
        self.BBgain_slider = BBgain_slider
        self.set_BB_gain(self.BBgain_slider)
        self._BBgain_slider_slider.set_value(self.BBgain_slider)
        self._BBgain_slider_text_box.set_value(self.BBgain_slider)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.osmosdr_source_1.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 50000, 1000000, firdes.WIN_HAMMING, 6.76))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.wxgui_fftsink2_0.set_baseband_freq(self.freq)
        self.osmosdr_source_1.set_center_freq(self.freq, 0)

    def get_RF_gain(self):
        return self.RF_gain

    def set_RF_gain(self, RF_gain):
        self.RF_gain = RF_gain
        self.osmosdr_source_1.set_gain(self.RF_gain, 0)

    def get_IF_gain(self):
        return self.IF_gain

    def set_IF_gain(self, IF_gain):
        self.IF_gain = IF_gain
        self.osmosdr_source_1.set_if_gain(self.IF_gain, 0)

    def get_BB_gain(self):
        return self.BB_gain

    def set_BB_gain(self, BB_gain):
        self.BB_gain = BB_gain
        self.osmosdr_source_1.set_bb_gain(self.BB_gain, 0)


def main(top_block_cls=airspy_FM, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
