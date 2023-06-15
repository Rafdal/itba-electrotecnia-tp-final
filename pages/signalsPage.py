from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from widgets.button import Button
from widgets.dropDownMenu import DropDownMenu
from PyQt5.QtCore import Qt
import numpy as np
from widgets.rectPlotBase import RectPlotBase

from libs.signals import *

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


        self.signalPlotWidget = FunctionPlotNav("Amplitud", dragable=True, resetScaleButton=True, resetJustY=True, xlabel="Tiempo [s]")
        self.signalPlotWidget.rectPlot.plotLabels = ["Output", "Input"]

        # Init plot
        x, yList = self.getData()
        self.signalPlotWidget.rectPlot.init_plot(x, yList)
        self.signalPlotWidget.rectPlot.draw_x_ticks(x)


        self.title = "Signal Editor"


        self.signalSettings = DynamicSettings(self.data.signal.params, lambda k,v: self.update_plot())

        signalMenu = DropDownMenu("Select Signal", False, self.onSignalChoose, self.data.signalOptions)

        vlayout.addWidget(signalMenu)
        vlayout.addWidget(self.signalSettings)


        def autoscale():
            self.signalPlotWidget.rectPlot.autoscale_x()
            self.signalPlotWidget.rectPlot.autoscale_y()


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
        # get frequency
        if 'f' in self.data.signal.params:
            f = self.data.signal.params['f'].value

        # check if stop is defined
        stop = 69.0
        if 'n_stop' in self.data.signal.params:
            n_stop = self.data.signal.params['n_stop'].value
            T = 1/f
            stop = n_stop*T

        if 't_stop' in self.data.signal.params:
            stop = self.data.signal.params['t_stop'].value

        t = np.linspace(0, stop, 5000, dtype=np.longdouble)

        x = self.data.signal(t)

        # simulate system
        lti = signal.lti(self.data.H.num, self.data.H.den)
        tout, y, _ = signal.lsim(lti, x, t)

        return t, [y, x]

    def update_plot(self):
        x, yList = self.getData()

        # self.signalPlotWidget.rectPlot.ax

        # clear previous plot
        # self.signalPlotWidget.rectPlot.clear_plot()

        self.signalPlotWidget.rectPlot.update_plot(x, yList)
        self.signalPlotWidget.rectPlot.autoscale_x()

        self.signalPlotWidget.rectPlot.draw_x_ticks(x)    
