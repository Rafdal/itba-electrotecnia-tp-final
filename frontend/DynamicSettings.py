from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from .slider import Slider
from decimal import Decimal

class DynamicSettings(QWidget):
    def __init__(self, settings_dict, onValueChanged=lambda k,v: None):
        super().__init__()
        self.settings_dict = settings_dict
        self.sliders = {}
        self.labels = {}
        self.onValueChanged = onValueChanged
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        for key, param in self.settings_dict.items():
            slider = Slider(0, 10)
            slider.setValue(param.value)
            slider.value_changed.connect(lambda value, key=key: self.updateParam(key, value))
            label = QLabel(f"{param.name} = {param.value} {param.unit}")
            layout.addWidget(label)
            layout.addWidget(slider)
            self.sliders[key] = slider
            self.labels[key] = label
        self.setLayout(layout)

    def updateParam(self, key, value):
        valueStr = Decimal(str(value)) / Decimal('100')
        self.settings_dict[key].value = value / 100.0
        self.onValueChanged(key, value)
        name = self.settings_dict[key].name
        unit = self.settings_dict[key].unit
        self.labels[key].setText(f"{name} = {valueStr} {unit}")