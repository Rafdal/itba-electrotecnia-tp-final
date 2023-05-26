from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from frontend.button import Button
from frontend.dropSwitchMenu import DropSwitchMenu
from PyQt5.QtCore import Qt
import numpy as np
from frontend.rectPlot import RectPlot
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


class FiltersPage(QVBoxLayout):
    def __init__(self, parent):
        super().__init__()

        # Create a layout for the widget
        vlayout = QVBoxLayout()

        hlayout = QHBoxLayout()
        hlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        vlayout = QVBoxLayout()
        vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Create a new RoundedRectPlot widget with a sine wave plot
        x = np.linspace(0, 6, 3000)
        u_x = 10**x
        y = np.abs(notch_filter(u_x, 300, 3))
        y = 20 * np.log10(y)

        plotWidget = RectPlot(x, y, title='My Plot', scale='log10', db=True)

        label = QLabel('Hello, PyQt5!', parent)

        button = Button("Center Plot", parent, 
            on_click = lambda: plotWidget.center_plot())
        button2 = Button("Reset Plot", parent, 
            on_click = lambda: plotWidget.reset_plot())
        button3 = Button("Autoscale Plot", parent,
            on_click = lambda: plotWidget.autoscale_plot())

        dropMenu = DropSwitchMenu(parent, options)

        slider = Slider(0, 4, 300, 20)
        slider.value_changed.connect(lambda value: self.update_plot(plotWidget, value))

        hlayout.addWidget(label)
        hlayout.addWidget(button)
        hlayout.addWidget(button2)
        hlayout.addWidget(button3)
        hlayout.addWidget(dropMenu)
        hlayout.addWidget(slider)

        vlayout.addLayout(hlayout)

        vlayout.addWidget(plotWidget)    

        self.addLayout(vlayout)

    def update_plot(self, plotWidget, value):
        # Update the plot with the new slider value
        x = np.linspace(0, 10, 1000)
        u_x = 10**x
        y = np.abs(notch_filter(u_x, 970, value))
        y = 20 * np.log10(y)
        plotWidget.update_plot(x, y)