from .rectPlotBase import RectPlotBase
from .button import Button
import numpy as np
from PyQt5.QtCore import Qt
from .slider import Slider
from .dropSwitchMenu import DropSwitchMenu
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QStyleFactory, QFrame

class FunctionPlotNav(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set the widget's properties using QStyle
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, Qt.white)
        self.setPalette(palette)
        self.setStyleSheet("border-radius: 10px;")
        self.setStyle(QStyleFactory.create('Fusion'))
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Set the widget's size
        self.setFixedSize(200, 100)

        # Set the widget's layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)

        # Add label widgets to the layout
        label1 = QLabel("Label 1")
        label2 = QLabel("Label 2")
        self.layout.addWidget(label1)
        self.layout.addWidget(label2)
