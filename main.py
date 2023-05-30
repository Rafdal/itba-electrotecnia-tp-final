import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QTabWidget

from pages.filtersPage import FiltersPage
from frontend.FunctionPlotNav import FunctionPlotNav

# Enable LaTeX rendering
import matplotlib as mpl

class ExampleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Example App')
        self.setGeometry(100, 100, 800, 800)

        tab_widget = QTabWidget()
        self.setCentralWidget(tab_widget)

        # create tabs
        filtersPage = FiltersPage(self)
        tab2 = QWidget()
        plotNav = FunctionPlotNav(self)

        # add tabs to tab widget
        tab_widget.addTab(filtersPage, filtersPage.title)
        tab_widget.addTab(plotNav, 'Tab 2')
        
        # add page


        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ExampleApp()
    sys.exit(app.exec_())