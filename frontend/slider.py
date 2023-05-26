from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QSlider, QVBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal

class Slider(QWidget):
    value_changed = pyqtSignal(float)

    def __init__(self, min_val, max_val, width, height, mult=100):
        super().__init__()
        self.min_val = min_val
        self.max_val = max_val
        self.mult = mult

        # create slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(self.min_val * self.mult)
        self.slider.setMaximum(self.max_val * self.mult)
        self.slider.setFixedWidth(width)
        self.slider.setFixedHeight(height)
        self.slider.valueChanged.connect(self.on_value_changed)

        self.initUI()

    def on_value_changed(self, value):
        self.value_changed.emit(self.get_value())

    def get_value(self):
        return float(self.slider.value()) / float(self.mult)

    def initUI(self):
        # create label to display slider value
        self.label = QLabel(str(self.get_value()))

        # create layout
        layout = QVBoxLayout()
        layout.addWidget(self.slider)
        layout.addWidget(self.label)
        self.setLayout(layout)

        # connect slider to label
        self.slider.valueChanged.connect(lambda: self.label.setText(str(self.get_value())))