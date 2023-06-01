from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from frontend.button import Button
from frontend.dropSwitchMenu import DropSwitchMenu
from PyQt5.QtCore import Qt
import numpy as np
from frontend.rectPlotBase import RectPlotBase

from backend.signals import *

from frontend.FunctionPlotNav import FunctionPlotNav
from frontend.DynamicSettings import DynamicSettings

from scipy import signal


class SignalsPage(QWidget):
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

        self.data = data

        self.signal = RectangularWave()


        self.signalPlotWidget = FunctionPlotNav("Amplitude", dragable=True)
        # self.phasePlotWidget = FunctionPlotNav("Phase", getData=getPhaseData, dragable=True, scale='log10', postFix="°")

        # Init plot
        x, yList = self.getData()
        self.signalPlotWidget.init_plot(x, yList)

        # self.magPlotWidget.setMinimumHeight(300)
        # self.phasePlotWidget.setMinimumHeight(300)

        self.title = "Signal Editor"


        self.signalSettings = DynamicSettings(self.signal.params, lambda k,v: self.update_plot())
        vlayout.addWidget(self.signalSettings)

        def autoscale():
            self.signalPlotWidget.rectPlot.autoscale_x()
            self.signalPlotWidget.rectPlot.autoscale_y()

        def printTransfer():
            print(self.data.H)

        button = Button("Autoscale", on_click=autoscale)
        button2 = Button("PrintTransfer", on_click=printTransfer)

        hlayoutPlots = QHBoxLayout()
        hlayoutPlots.setContentsMargins(0, 0, 0, 0)
        hlayoutPlots.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hlayoutPlots.addWidget(button)
        hlayoutPlots.addWidget(button2)
        vlayoutPlots.addLayout(hlayoutPlots)
        vlayoutPlots.addWidget(self.signalPlotWidget)    
        vlayoutPlots.setStretch(1, 1)
        
        hlayout.addLayout(vlayout)
        hlayout.addLayout(vlayoutPlots)
        hlayout.setStretch(1, 1)

        self.setLayout(hlayout)

    def on_tab_focus(self):
        print("on_tab_focus")
        self.update_plot()

    # Create x and y data getter
    def getData(self):
        t = np.linspace(0, 6 * np.pi, 3000)
        x = self.signal(t)

        # simulate system
        lti = signal.lti(self.data.H.num, self.data.H.den)
        tout, y, _ = signal.lsim(lti, x, t)

        return t, [y, x]

    def update_plot(self):
        x, yList = self.getData()
        self.signalPlotWidget.rectPlot.update_plot(x, yList)
        # self.phasePlotWidget.update_plot()