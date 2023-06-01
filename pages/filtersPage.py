from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from frontend.button import Button
from frontend.dropSwitchMenu import DropSwitchMenu
from PyQt5.QtCore import Qt
import numpy as np
from frontend.rectPlotBase import RectPlotBase

from backend.filters import *

from frontend.FunctionPlotNav import FunctionPlotNav
from frontend.DynamicSettings import DynamicSettings

from scipy import signal

import warnings
import traceback

class FiltersPage(QWidget):
    def __init__(self, data):
        super().__init__()

        # Create a layout for the widget
        hlayout = QHBoxLayout()
        hlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hlayout.setStretch(0, 1)
        vlayoutPlots = QVBoxLayout()
        vlayoutPlots.setAlignment(Qt.AlignmentFlag.AlignTop)
        vlayout = QVBoxLayout()
        vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.notch = NotchFilter(300.0, 2.0)
        self.filter2 = SOLowPass()

        self.data = data

        self.filters = [
            # self.notch,
            self.filter2
        ]

        self.magPlotWidget = FunctionPlotNav("Magnitude", dragable=True, scale='log10', postFix="dB", yInitRange=200.0)
        self.phasePlotWidget = FunctionPlotNav("Phase", dragable=True, scale='log10', postFix="°", yInitRange=420.0)
        

        self.magPlotWidget.setMinimumHeight(300)
        self.phasePlotWidget.setMinimumHeight(300)

        # Compute and init plots
        x, mag, phase = self.computePlot()
        self.phasePlotWidget.init_plot(x, [phase])
        self.magPlotWidget.init_plot(x, [mag])

        self.title = "Filter Editor"


        self.filterSettings = DynamicSettings(self.filter2.params, lambda k,v: self.update_plot())
        vlayout.addWidget(self.filterSettings)

        def autoscale():
            self.magPlotWidget.rectPlot.autoscale_x()
            self.magPlotWidget.rectPlot.autoscale_y()
            self.phasePlotWidget.rectPlot.autoscale_x()
            self.phasePlotWidget.rectPlot.autoscale_y()
        button = Button("Autoscale", on_click=autoscale)

        hlayoutPlots = QHBoxLayout()
        hlayoutPlots.setContentsMargins(0, 0, 0, 0)
        hlayoutPlots.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hlayoutPlots.addWidget(button)
        vlayoutPlots.addLayout(hlayoutPlots)
        vlayoutPlots.addWidget(self.magPlotWidget)    
        vlayoutPlots.addWidget(self.phasePlotWidget)
        vlayoutPlots.setStretch(1, 1)
        vlayoutPlots.setStretch(2, 1)
        
        hlayout.addLayout(vlayout)
        hlayout.addLayout(vlayoutPlots)
        hlayout.setStretch(1, 1)

        self.setLayout(hlayout)

    def computePlot(self, n=3000, x0=0.0, x1=6.0, base=10.0):
        x = np.linspace(x0, x1, n)
        wlog_x = base**x

        F = Filter()
        for f in self.filters:
            F = F * f

        self.data.H = F.transfer()
        _, mag, phase = signal.bode(self.data.H, wlog_x, n)

        return x, mag, phase

    def update_plot(self):
        x, mag, phase = self.computePlot()

        self.phasePlotWidget.rectPlot.update_plot(x, [phase])
        self.magPlotWidget.rectPlot.update_plot(x, [mag])