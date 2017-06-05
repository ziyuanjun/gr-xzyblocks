#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Airspy Scan2
# Generated: Mon May 22 15:10:19 2017
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

from PyQt4 import Qt
from PyQt4.QtGui import QComboBox
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import sip
import sys
import time
import xzyblocks
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

class airspy_scan2(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Airspy Scan2")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Airspy Scan2")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "airspy_scan2")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2500000
        #self.samp_rate = samp_rate = 2500000 * 4
        self.freq = freq = 88e6

        ##################################################
        # Blocks
        ##################################################

        paraLayout = Qt.QHBoxLayout()
        samprateLabel = Qt.QLabel("f<sub>s</sub>:")
        self.samprateComboBox = QComboBox()
        self.samprateComboBox.addItems(["2.5M", "10M"])
        freqMinLabel = Qt.QLabel("f<sub>min</sub>(MHz):")
        self.freqMinSpinBox=Qt.QSpinBox()
        #self.freqMinSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.freqMinSpinBox.setRange(30,1000)
        freqMaxLabel = Qt.QLabel("f<sub>max</sub>(MHz):")
        self.freqMaxSpinBox=Qt.QSpinBox()
        #self.freqMaxSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.freqMaxSpinBox.setRange(40,1010)
        self.saveCheckBox = Qt.QCheckBox("save raw IQ")
        paraLayout.addStretch()
        paraLayout.addWidget(samprateLabel)
        paraLayout.addWidget(self.samprateComboBox)
        paraLayout.addWidget(freqMinLabel)
        paraLayout.addWidget(self.freqMinSpinBox)
        paraLayout.addWidget(freqMaxLabel)
        paraLayout.addWidget(self.freqMaxSpinBox)
        paraLayout.addWidget(self.saveCheckBox)

        self.top_layout.addLayout(paraLayout)
        self.osmosdr_source_1 = osmosdr.source( args="numchan=" + str(1) + " " + 'airspy' )
        self.osmosdr_source_1.set_sample_rate(samp_rate)
        self.osmosdr_source_1.set_center_freq(freq, 0)
        self.osmosdr_source_1.set_freq_corr(0, 0)
        self.osmosdr_source_1.set_dc_offset_mode(0, 0)
        self.osmosdr_source_1.set_iq_balance_mode(0, 0)
        self.osmosdr_source_1.set_gain_mode(False, 0)
        self.osmosdr_source_1.set_gain(10, 0)
        self.osmosdr_source_1.set_if_gain(20, 0)
        self.osmosdr_source_1.set_bb_gain(20, 0)
        self.osmosdr_source_1.set_antenna('', 0)
        self.osmosdr_source_1.set_bandwidth(0, 0)

        freqMin,freqMax=88e6,108e6
        # freqMin,freqMax=400e6,420e6
        # freqMin,freqMax=118e6,136e6
        #freqMin,freqMax=40e6,800e6
        freqCenter=freqMin
        self.osmosdr_source_1.set_center_freq(freqCenter, 0)
        self.xzyblocks_fft_scan_plot_py_vc_0 = xzyblocks.fft_scan_plot_py_vc(self.osmosdr_source_1, samp_rate, 1024, freqCenter, freqMin, freqMax,25,512,alpha=0.1)
        #self.xzyblocks_fft_scan_plot_py_vc_0 = xzyblocks.fft_scan_plot_py_vc()
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, 1024)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_stream_to_vector_0, 0), (self.xzyblocks_fft_scan_plot_py_vc_0, 0))
        self.connect((self.osmosdr_source_1, 0), (self.blocks_stream_to_vector_0, 0))
        #self.connect((self.osmosdr_source_1, 0), (self.qtgui_time_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "airspy_scan2")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        #self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.osmosdr_source_1.set_sample_rate(self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_source_1.set_center_freq(self.freq, 0)

win = pg.GraphicsWindow(title="Basic plotting examples")
win.resize(1000,600)
pg.setConfigOptions(antialias=True)
p6 = win.addPlot(title="Scanning")
curve = p6.plot(pen='y')
ptr=0
def main(top_block_cls=airspy_scan2, options=None):
    global curve, ptr, p6

    alpha=0.1
    qapp=QtGui.QApplication.instance()

    tb = top_block_cls()
    tb.top_layout.addWidget(win)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    def update():
        global curve, ptr, p6
        if ptr>=1:
            data=np.abs(tb.xzyblocks_fft_scan_plot_py_vc_0.plotData)
            data[data<1e-6]=1e-6
            ydata=20*np.log10(data)
            curve.setData(x=tb.xzyblocks_fft_scan_plot_py_vc_0.xaxisData/1000000.0,y=ydata)
        elif ptr==1:
            p6.enableAutoRange('xy', False)
        ptr += 1

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(50)
    print np.shape(tb.xzyblocks_fft_scan_plot_py_vc_0.plotData)
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
