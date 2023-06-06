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
    def __init__(self, title = 'Title', dragable = False, scale = 'linear', postFix = None, 
                 yInitRange=20.0, resetScaleButton = True, xlabel = None, plotLabels = []):
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


        # Add Widgets
        self.rectPlot = RectPlotBase(dragable, scale, postFix=postFix, yInitRange=yInitRange, xlabel=xlabel, plotLabels=plotLabels)
        self.rectPlot.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        button1 = Button("Autoscale X", None, on_click=lambda: self.rectPlot.autoscale_x())
        button2 = Button("Autoscale Y", None, on_click=lambda: self.rectPlot.autoscale_y())
       
        button3 = None
        if resetScaleButton:
            button3 = Button("Reset Scale", None, on_click=lambda: self.rectPlot.reset_plot())
        
        label = QLabel(title)
        label.setStyleSheet("""
            font-size: 18px;
            background-color: transparent;
            color: black;
        """)
        hlayout = QHBoxLayout()
        hlayout.setContentsMargins(3, 3, 3, 0)

        hlayout.addWidget(button1)
        hlayout.addWidget(button2)
        if button3 is not None:
            hlayout.addWidget(button3)

        titleLayout = QHBoxLayout()
        titleLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titleLayout.setContentsMargins(0, 0, 0, 0)
        titleLayout.setSpacing(0)
        titleLayout.addStretch(1)
        titleLayout.addWidget(label)
        titleLayout.addStretch(1)

        hlayout.addStretch(1)
        hlayout.addLayout(titleLayout)
        hlayout.addStretch(1)

        layout.addLayout(hlayout)
        layout.addWidget(self.rectPlot)
        layout.setContentsMargins(0, 0, 0, 0)

        frame.setLayout(layout)
        mainLayout.addWidget(frame)

    def init_plot(self, x, yList):
        self.rectPlot.init_plot(x, yList)

    def update_plot(self, x, yList):
        self.rectPlot.update_plot(x, yList)