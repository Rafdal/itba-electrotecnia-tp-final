from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from frontend.button import Button
from frontend.dropSwitchMenu import DropSwitchMenu
from PyQt5.QtCore import Qt
import numpy as np
from frontend.rectPlotBase import RectPlotBase
from frontend.slider import Slider

from backend.filters import Filter, NotchFilter

from frontend.FunctionPlotNav import FunctionPlotNav

from scipy import signal


class FiltersPage(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        # Create a layout for the widget
        hlayout = QHBoxLayout()
        hlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hlayout.setStretch(0, 1)
        vlayoutPlots = QVBoxLayout()
        vlayoutPlots.setAlignment(Qt.AlignmentFlag.AlignTop)
        vlayout = QVBoxLayout()
        vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.slider = Slider(0, 4)
        self.slider2 = Slider(-1, 5)
        self.slider.slider.setValue(24)
        self.slider2.slider.setValue(300)
        self.slider.value_changed.connect(self.update_plot)
        self.slider2.value_changed.connect(self.update_plot)

        self.notch = NotchFilter(300.0, 2.0)

        self.filters = [
            self.notch,
        ]

        def getMagData():
            print("getMagData")
            x, mag, _ = self.computePlot()
            return x, [mag]
        
        def getPhaseData():
            print("getPhaseData")
            x, _, phase = self.computePlot()
            return x, [phase]

        self.magPlotWidget = FunctionPlotNav("Magnitude", getData=getMagData,dragable=True, scale='log10', db=True)
        self.phasePlotWidget = FunctionPlotNav("Phase", getData=getPhaseData, dragable=True, scale='log10', db=False)

        self.magPlotWidget.setMinimumHeight(300)
        self.phasePlotWidget.setMinimumHeight(300)

        self.title = "Filter Editor"


        vlayout.addWidget(self.slider)
        vlayout.addWidget(self.slider2)

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

        self.notch.w0 = 10.0 ** self.slider2.get_value()
        self.notch.xi = self.slider.get_value()

        F = Filter()
        for f in self.filters:
            F = F * f
        _, mag, phase = signal.bode(F.transfer(), wlog_x, n)

        return x, mag, phase

    def update_plot(self):
        x, mag, phase = self.computePlot()

        self.phasePlotWidget.rectPlot.update_plot(x, [phase])
        self.magPlotWidget.rectPlot.update_plot(x, [mag])