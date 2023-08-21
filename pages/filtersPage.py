from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from widgets.button import Button
from widgets.dropDownMenu import DropDownMenu
from PyQt5.QtCore import Qt
import numpy as np
from widgets.rectPlotBase import RectPlotBase

from libs.filters import *

from widgets.FunctionPlotNav import FunctionPlotNav
from widgets.ZerosPolesPlot import ZerosPolesPlot
from widgets.DynamicSettings import DynamicSettings
from widgets.DynamicWidgetList import DynamicWidgetList

from scipy import signal


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

        self.magPlotWidget = FunctionPlotNav("Ganancia [dB]", dragable=True, scale='log10', postFix="dB", yInitRange=200.0, xlabel="Frecuencia [Hz]")
        self.phasePlotWidget = FunctionPlotNav("Fase [°]", dragable=True, scale='log10', postFix="°", yInitRange=420.0, xlabel="Frecuencia [Hz]")
        self.polesZerosPlotWidget = ZerosPolesPlot(data=self.data)

        self.magPlotWidget.setMinimumHeight(300)
        self.phasePlotWidget.setMinimumHeight(300)

        # Compute and init plots
        x, mag, phase = self.computePlot()

        self.phasePlotWidget.init_plot(x, [phase])
        self.magPlotWidget.init_plot(x, [mag])

        self.title = "Filter Editor"

        self.filterSettings = DynamicSettings({}, lambda k,v: self.update_plot())
        self.filterSettings.setMaximumWidth(400)

        self.filterList = DynamicWidgetList(self.data.filters, self.onFilterClick, self.onFilterDelete)
        self.filterList.setMinimumHeight(180)
        self.filterList.setMinimumWidth(150)
        self.filterList.setMaximumWidth(400)

        self.filterMenu = DropDownMenu(
            options=self.data.filterOptions, 
            onChoose=self.onFilterChoose,
            title="Select Filter"
        )
        self.filterMenu.setMinimumWidth(150)
        self.filterMenu.setMaximumWidth(400)

        self.data.on_filter_close = self.update_plot

        vlayout.addWidget(QLabel("Add Filters"))
        vlayout.addWidget(self.filterMenu)
        vlayout.addWidget(self.filterList)

        vlayout.addWidget(self.filterSettings)
        vlayout.addWidget(self.polesZerosPlotWidget)
        # vlayout.addStretch(0)


        hlayoutPlots = QHBoxLayout()
        hlayoutPlots.setContentsMargins(0, 0, 0, 0)
        hlayoutPlots.setAlignment(Qt.AlignmentFlag.AlignLeft)
        vlayoutPlots.addLayout(hlayoutPlots)
        vlayoutPlots.addWidget(self.magPlotWidget)    
        vlayoutPlots.addWidget(self.phasePlotWidget)
        vlayoutPlots.setStretch(1, 1)
        vlayoutPlots.setStretch(2, 1)
        
        hlayout.addLayout(vlayout)
        hlayout.addLayout(vlayoutPlots)
        hlayout.setStretch(1, 1)
        hlayout.setStretch(2, 1)

        self.setLayout(hlayout)

    # def onFilterClose(self):


    def onFilterChoose(self):
        self.filterList.render_widgets()
        print( self.data.F.num, self.data.F.den)
        if len(self.data.filters) > 0:
            self.selectedFilter = self.data.filters[-1]
            self.filterSettings.update(self.selectedFilter.params, self.selectedFilter.name + " Settings")
        else:
            self.selectedFilter = None
            self.filterSettings.update({}, "")

        self.update_plot()

    def on_tab_focus(self):
        pass

    def onFilterClick(self, idx, value):
        self.selectedFilter = self.data.filters[idx]
        if self.selectedFilter.callback is not None:
            self.selectedFilter.callback()
            # hide the settings widget
            self.filterSettings.setVisible(False)
        else:
            self.filterSettings.setVisible(True)
            self.filterSettings.update(self.selectedFilter.params, self.selectedFilter.name + " Settings")
        print("click", idx, value)

    def onFilterDelete(self, idx, value):
        print("delete", idx, value)
        self.data.filters.pop(idx)
        self.filterList.render_widgets()
        if len(self.data.filters) > 0:
            self.selectedFilter = self.data.filters[-1]
            self.filterSettings.update(self.selectedFilter.params, self.selectedFilter.name + " Settings")
        else:
            self.selectedFilter = None
            self.filterSettings.update({}, "")
        self.update_plot()


    def computePlot(self, n=8000, x0=-2.0, x1=8.0, base=10.0):
        print("computePlot")
        # f0 = Param(-2.0, "Start Frequency", "Hz", range=[-3.0, 3.0])
        # f1 = Param(6.0, "End Frequency", "Hz", range=[4.0, 12.0])

        x = np.linspace(x0, x1, n)
        flog_x = base**x
        # wlog_x = 2.0 * np.pi * flog_x
        wlog_x = base**x

        F = Filter()
        for f in self.data.filters:
            F = F * f

        self.data.F = F
        self.data.H = F.transfer()
        _, mag, phase = signal.bode(self.data.H, wlog_x, n)

        return x, mag, phase

    def update_plot(self):
        x, mag, phase = self.computePlot()

        self.phasePlotWidget.rectPlot.update_plot(x, [phase])
        self.magPlotWidget.rectPlot.update_plot(x, [mag])

        self.polesZerosPlotWidget.on_tab_focus()