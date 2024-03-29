from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QSlider, QVBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal

class Slider(QWidget):
    value_changed = pyqtSignal(float)

    def __init__(self, min_val, max_val, width=300, height=10, mult=100, show_label=False):
        super().__init__()
        self.min_val = min_val
        self.max_val = max_val
        self.mult = mult
        self.show_label = show_label

        # create slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(int(self.min_val * self.mult))
        self.slider.setMaximum(int(self.max_val * self.mult))
        self.slider.setFixedWidth(width)
        self.slider.setFixedHeight(height)
        self.slider.valueChanged.connect(self.on_value_changed)

        self.initUI()

    def on_value_changed(self, value):
        self.value_changed.emit(self.get_value())

    def get_value(self):
        return float(self.slider.value()) / float(self.mult)
    
    def setValue(self, value):
        try:
            self.slider.setValue(int(value * self.mult))
        except:
            print("Slider: value out of range")
            print("Slider: value = ", value)
            self.slider.setValue(int((self.max_val - self.min_val) * self.mult * 0.5))

    def initUI(self):
        # create label to display slider value
        if self.show_label:
            self.label = QLabel(str(self.get_value()))

        # create layout
        layout = QVBoxLayout()
        layout.addWidget(self.slider)
        if self.show_label:
            layout.addWidget(self.label)
            # connect slider to label
            self.slider.valueChanged.connect(lambda: self.label.setText(str(self.get_value())))
        self.setLayout(layout)
