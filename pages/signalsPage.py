from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from widgets.button import Button
from widgets.dropDownMenu import DropDownMenu
from PyQt5.QtCore import Qt
import numpy as np
from widgets.rectPlotBase import RectPlotBase

from backend.signals import *

from widgets.FunctionPlotNav import FunctionPlotNav
from widgets.DynamicSettings import DynamicSettings
from widgets.DynamicWidgetList import DynamicWidgetList

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


        self.signalPlotWidget = FunctionPlotNav("Amplitude", dragable=True)
        # self.phasePlotWidget = FunctionPlotNav("Phase", getData=getPhaseData, dragable=True, scale='log10', postFix="°")

        # Init plot
        x, yList = self.getData()
        self.signalPlotWidget.init_plot(x, yList)

        # self.magPlotWidget.setMinimumHeight(300)
        # self.phasePlotWidget.setMinimumHeight(300)

        self.title = "Signal Editor"


        self.signalSettings = DynamicSettings(self.data.signal.params, lambda k,v: self.update_plot())

        signalMenu = DropDownMenu("Select Signal", False, self.onSignalChoose, self.data.signalOptions)

        vlayout.addWidget(signalMenu)
        vlayout.addWidget(self.signalSettings)


        def autoscale():
            self.signalPlotWidget.rectPlot.autoscale_x()
            self.signalPlotWidget.rectPlot.autoscale_y()

        def printTransfer():
            print(self.data.H)

        button = Button("Autoscale", on_click=autoscale)

        hlayoutPlots = QHBoxLayout()
        hlayoutPlots.setContentsMargins(0, 0, 0, 0)
        hlayoutPlots.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hlayoutPlots.addWidget(button)
        vlayoutPlots.addLayout(hlayoutPlots)
        vlayoutPlots.addWidget(self.signalPlotWidget)    
        vlayoutPlots.setStretch(1, 1)
        
        hlayout.addLayout(vlayout)
        hlayout.addLayout(vlayoutPlots)
        hlayout.setStretch(1, 1)

        self.setLayout(hlayout)

    def onSignalChoose(self):
        self.signalSettings.update(self.data.signal.params)
        self.update_plot()

    def onDelete(self, key, name):
        print("onDelete", key, name)


    def on_tab_focus(self):
        print("on_tab_focus")
        self.update_plot()

    # Create x and y data getter
    def getData(self):
        t = np.linspace(0, 6 * np.pi, 3000)
        x = self.data.signal(t)

        # simulate system
        lti = signal.lti(self.data.H.num, self.data.H.den)
        tout, y, _ = signal.lsim(lti, x, t)

        return t, [y, x]

    def update_plot(self):
        x, yList = self.getData()
        self.signalPlotWidget.rectPlot.update_plot(x, yList)
        # self.phasePlotWidget.update_plot()