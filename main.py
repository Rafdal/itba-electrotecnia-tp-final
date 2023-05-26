import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QTabWidget

from pages.filtersPage import FiltersPage

class ExampleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Example App')
        self.setGeometry(100, 100, 800, 600)

        tab_widget = QTabWidget()
        self.setCentralWidget(tab_widget)

        # create tabs
        tab1 = QWidget()
        tab2 = QWidget()

        # add tabs to tab widget
        tab_widget.addTab(tab1, 'Tab 1')
        tab_widget.addTab(tab2, 'Tab 2')

        # add page
        filtersPage = FiltersPage(self)

        tab1.setLayout(filtersPage)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ExampleApp()
    sys.exit(app.exec_())