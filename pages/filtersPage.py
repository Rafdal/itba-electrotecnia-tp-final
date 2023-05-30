from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from frontend.button import Button
from frontend.dropSwitchMenu import DropSwitchMenu
from PyQt5.QtCore import Qt
import numpy as np
from frontend.rectPlotBase import RectPlotBase
from frontend.slider import Slider

from backend.filters import notch_filter

options = [
    {
        'name': 'Option 1',
        'callback': lambda: print('Option 1')
    },
    {
        'name': 'Option 2',
        'callback': lambda: print('Option 2')
    },
    {
        'name': 'Option 3',
        'callback': lambda: print('Option 3')
    }
]

from scipy import signal


class FiltersPage(QWidget):
    def __init__(self, parent):
        super().__init__()

        # Create a layout for the widget
        vlayout = QVBoxLayout()

        hlayout = QHBoxLayout()
        hlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        vlayout = QVBoxLayout()
        vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        n = 3000
        x = np.linspace(0, 6, n)
        wlog_x = 10**x
        H = notch_filter(300, 3)
        _, mag, phase = signal.bode(H, wlog_x, n)
        y = mag

        self.magPlotWidget = RectPlotBase(x, [y], title='Ganancia dB', scale='log10', db=True)
        self.phasePlotWidget = RectPlotBase(x, [phase], title='Fase', scale='log10', db=False)

        self.title = "Filter Editor"

        button = Button("Center Plot", parent, 
            on_click = lambda: self.magPlotWidget.center_plot())
        button2 = Button("Reset Plot", parent, 
            on_click = lambda: self.magPlotWidget.reset_plot())
        button3 = Button("Autoscale X", parent,
            on_click = lambda: self.magPlotWidget.autoscale_x())

        button4 = Button("Autoscale Y", parent,
                    on_click = lambda: self.magPlotWidget.autoscale_y())

        dropMenu = DropSwitchMenu(parent, options)

        slider = Slider(0, 4, 300, 20)
        slider.value_changed.connect(lambda value: self.update_plot(value))

        hlayout.addWidget(button)
        hlayout.addWidget(button2)
        hlayout.addWidget(button3)
        hlayout.addWidget(button4)
        hlayout.addWidget(dropMenu)
        hlayout.addWidget(slider)

        vlayout.addLayout(hlayout)

        vlayout.addWidget(self.magPlotWidget)    
        vlayout.addWidget(self.phasePlotWidget)

        self.setLayout(vlayout)

    def update_plot(self, value):
        
        n = 3000
        x = np.linspace(0, 6, n)
        wlog_x = 10**x
        H = notch_filter(300, value)
        _, mag, phase = signal.bode(H, wlog_x, n)
        y = mag

        self.magPlotWidget.update_plot(x, [y])
        self.phasePlotWidget.update_plot(x, [phase])