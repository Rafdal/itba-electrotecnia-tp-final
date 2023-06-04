import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QTabWidget

from pages.filtersPage import FiltersPage
from pages.signalsPage import SignalsPage

import matplotlib as mpl
import numpy as np

from scipy import signal

from backend.utils import Param

from models.dataModel import DataModel

class ExampleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Example App')
        self.setGeometry(100, 100, 100, 100)

        tab_widget = QTabWidget()
        self.setCentralWidget(tab_widget)

        # create a Data Model
        self.dataModel = DataModel()

        # create tabs
        filtersPage = FiltersPage(data=self.dataModel)
        signalsPage = SignalsPage(data=self.dataModel)

        # add tabs to tab widget
        tab_widget.addTab(filtersPage, filtersPage.title)
        tab_widget.addTab(signalsPage, signalsPage.title)

        # set tab content background color
        tab_widget.setStyleSheet("QWidget { background-color: #f5f5f5 }")

        tab_widget.currentChanged.connect(self.tab_changed)


        self.show()

    def tab_changed(self, index):
        # get newly active tab
        tab_widget = self.centralWidget()
        current_widget = tab_widget.widget(index)

        # check if method exists
        if hasattr(current_widget, 'on_tab_focus'): 
            current_widget.on_tab_focus()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ExampleApp()
    sys.exit(app.exec_())