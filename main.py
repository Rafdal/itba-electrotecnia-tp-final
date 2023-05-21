import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout
from frontend.button import Button
from frontend.dropMenu import DropMenu
from PyQt5.QtCore import Qt

import numpy as np
from frontend.rectPlot import RectPlot


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

class ExampleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Example App')
        self.setGeometry(100, 100, 800, 600)

        hlayout = QHBoxLayout()
        hlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        vlayout = QVBoxLayout()
        vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Create a new RoundedRectPlot widget with a sine wave plot
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        plotWidget = RectPlot(x, y, title='My Plot')

        label = QLabel('Hello, PyQt5!', self)

        button = Button("Center Plot", self, 
            on_click = lambda: plotWidget.center_plot())
        button2 = Button("Reset Plot", self, 
            on_click = lambda: plotWidget.reset_plot())

        dropMenu = DropMenu(self, options)

        hlayout.addWidget(label)
        hlayout.addWidget(button)
        hlayout.addWidget(button2)
        hlayout.addWidget(dropMenu)

        vlayout.addLayout(hlayout)

        vlayout.addWidget(plotWidget)

        central_widget = QWidget()
        central_widget.setLayout(vlayout)
        self.setCentralWidget(central_widget)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ExampleApp()
    sys.exit(app.exec_())