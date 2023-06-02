from .rectPlotBase import RectPlotBase
from .button import Button
import numpy as np
from PyQt5.QtCore import Qt
from .slider import Slider
from .dropDownMenu import DropDownMenu
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsDropShadowEffect, QFrame
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QSizePolicy

class FunctionPlotNav(QWidget):
    def __init__(self, title = 'Title', dragable = False, scale = 'linear', postFix = None, yInitRange=20.0):
        super().__init__()

        mainLayout = QVBoxLayout(self)
        mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        mainLayout.setContentsMargins(5, 5, 5, 5)
        mainLayout.setSpacing(0)

        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.Box)
        frame.setContentsMargins(5, 5, 5, 5)
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        frame.setStyleSheet("""
            .QFrame{
                background-color: white; 
                border-radius: 12px;
            }""")
        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor("grey"))
        shadow.setOffset(0, 0)
        shadow.setBlurRadius(14)
        frame.setGraphicsEffect(shadow)

        # Set the widget's layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(3, 3, 3, 0)
        # layout.setSpacing(10)

        hlayout = QHBoxLayout()
        hlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hlayout.setContentsMargins(3, 3, 3, 0)

        # Add Widgets
        self.rectPlot = RectPlotBase(dragable, scale, postFix=postFix, yInitRange=yInitRange)
        self.rectPlot.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        button1 = Button("Autoscale X", None, on_click=lambda: self.rectPlot.autoscale_x())
        button2 = Button("Autoscale Y", None, on_click=lambda: self.rectPlot.autoscale_y())
        button3 = Button("Reset Scale", None, on_click=lambda: self.rectPlot.reset_plot())
        
        label = QLabel(title)
        label.setStyleSheet("""
            font-size: 18px;
            background-color: transparent;
            color: black;
            """)

        hlayout.addWidget(button1)
        hlayout.addWidget(button2)
        hlayout.addWidget(button3)
        hlayout.addWidget(label)

        layout.addLayout(hlayout)
        layout.addWidget(self.rectPlot)
        layout.setContentsMargins(0, 0, 0, 0)

        frame.setLayout(layout)
        mainLayout.addWidget(frame)

    def init_plot(self, x, yList):
        self.rectPlot.init_plot(x, yList)

    def update_plot(self, x, yList):
        self.rectPlot.update_plot(x, yList)