from .rectPlotBase import RectPlotBase
from .button import Button
import numpy as np
from PyQt5.QtCore import Qt
from .slider import Slider
from .dropSwitchMenu import DropSwitchMenu
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsDropShadowEffect, QFrame
from PyQt5.QtGui import QColor


class FunctionPlotNav(QWidget):
    def __init__(self, parent=None, title = 'Title', 
                 getData = lambda: (np.array([1,2]), [np.array([0,4])]), 
                 dragable = False, scale = 'linear', db = False):
        super().__init__(parent)

        frame = QFrame(self)
        frame.setFrameShape(QFrame.Shape.Box)
        frame.setContentsMargins(5, 5, 5, 5)

        frame.setStyleSheet("""
            .QFrame{
                background-color: white; 
                border-radius: 10px;
            }""")
        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor("grey"))
        shadow.setOffset(0, 0)
        shadow.setBlurRadius(8)
        frame.setGraphicsEffect(shadow)

        # Set the widget's layout
        layout = QVBoxLayout()
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(10)

        hlayout = QHBoxLayout()
        hlayout.setContentsMargins(3, 3, 3, 3)
        hlayout.setSpacing(5)

        # Add Widgets
        self.getData = getData
        x, yList = self.getData()
        self.rectPlot = RectPlotBase(x, yList, title, dragable, scale, db)
        button1 = Button("Autoscale X", parent,
                            on_click=lambda: self.rectPlot.autoscaleX())
        button2 = Button("Zoom Out", parent,
                            on_click=lambda: self.rectPlot.zoomOut())

        hlayout.addWidget(button1)
        hlayout.addWidget(button2)

        layout.addLayout(hlayout)
        layout.addWidget(self.rectPlot)

        frame.setLayout(layout)

    def setData(self, x, yList):
        self.x = x
        self.yList = yList
        self.updatePlot()
