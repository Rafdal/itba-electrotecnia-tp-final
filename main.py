import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QTabWidget

from pages.filtersPage import FiltersPage
from frontend.FunctionPlotNav import FunctionPlotNav

import matplotlib as mpl
import numpy as np

class ExampleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Example App')
        self.setGeometry(100, 100, 800, 800)

        tab_widget = QTabWidget()
        self.setCentralWidget(tab_widget)

        # Create x and y data getter
        def getData():
            x = np.linspace(0, 6 * np.pi, 100)
            y = 4*np.sin(x)+0.6
            return x, [y]

        # create tabs
        filtersPage = FiltersPage()
        tab2 = QWidget()
        plotNav = FunctionPlotNav("Title", getData=getData, dragable=True)

        # add tabs to tab widget
        tab_widget.addTab(filtersPage, filtersPage.title)
        tab_widget.addTab(plotNav, 'Tab 2')
        
        # set tab content background color
        tab_widget.setStyleSheet("QWidget { background-color: #f5f5f5 }")


        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ExampleApp()
    sys.exit(app.exec_())