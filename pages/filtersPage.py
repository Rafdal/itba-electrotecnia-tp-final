from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from widgets.button import Button
from widgets.dropDownMenu import DropDownMenu
from PyQt5.QtCore import Qt
import numpy as np
from widgets.rectPlotBase import RectPlotBase

from backend.filters import *

from widgets.FunctionPlotNav import FunctionPlotNav
from widgets.DynamicSettings import DynamicSettings
from widgets.DynamicWidgetList import DynamicWidgetList

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

        self.data = data

        self.selectedFilter = None

        self.magPlotWidget = FunctionPlotNav("Magnitude", dragable=True, scale='log10', postFix="dB", yInitRange=200.0)
        self.phasePlotWidget = FunctionPlotNav("Phase", dragable=True, scale='log10', postFix="°", yInitRange=420.0)
        

        self.magPlotWidget.setMinimumHeight(300)
        self.phasePlotWidget.setMinimumHeight(300)

        # Compute and init plots
        x, mag, phase = self.computePlot()
        self.phasePlotWidget.init_plot(x, [phase])
        self.magPlotWidget.init_plot(x, [mag])

        self.title = "Filter Editor"

        self.filterSettings = DynamicSettings({}, lambda k,v: self.update_plot())

        self.filterList = DynamicWidgetList(self.data.filters, self.onFilterClick, self.onFilterDelete)
        self.filterList.setMinimumHeight(200)
        self.filterList.setMinimumWidth(150)

        self.filterMenu = DropDownMenu(options=self.data.filterOptions, onChoose=self.onFilterChoose)

        vlayout.addWidget(QLabel("Add Filters"))
        vlayout.addWidget(self.filterMenu)
        vlayout.addWidget(self.filterList)

        vlayout.addWidget(self.filterSettings)
        vlayout.addStretch(0)

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

    def onFilterChoose(self):
        self.filterList.render_widgets()
        if len(self.data.filters) > 0:
            self.selectedFilter = self.data.filters[-1]
            self.filterSettings.update(self.selectedFilter.params)
        else:
            self.selectedFilter = None
            self.filterSettings.update({})

        self.update_plot()

    def onFilterClick(self, idx, value):
        self.selectedFilter = self.data.filters[idx]
        self.filterSettings.update(self.selectedFilter.params)
        print("click", idx, value)

    def onFilterDelete(self, idx, value):
        print("delete", idx, value)
        self.data.filters.pop(idx)
        self.filterList.render_widgets()
        if len(self.data.filters) > 0:
            self.selectedFilter = self.data.filters[-1]
            self.filterSettings.update(self.selectedFilter.params)
        else:
            self.selectedFilter = None
            self.filterSettings.update({})
        self.update_plot()


    def computePlot(self, n=3000, x0=0.0, x1=6.0, base=10.0):
        # f0 = Param(-2.0, "Start Frequency", "Hz", range=[-3.0, 3.0])
        # f1 = Param(6.0, "End Frequency", "Hz", range=[4.0, 12.0])

        x = np.linspace(x0, x1, n)
        wlog_x = base**x

        F = Filter()
        for f in self.data.filters:
            F = F * f

        self.data.H = F.transfer()
        _, mag, phase = signal.bode(self.data.H, wlog_x, n)

        # get poles and zeros
        poles, zeros, _ = F.getPolesAndZeroes()

        return x, mag, phase

    def update_plot(self):
        x, mag, phase = self.computePlot()

        self.phasePlotWidget.rectPlot.update_plot(x, [phase])
        self.magPlotWidget.rectPlot.update_plot(x, [mag])