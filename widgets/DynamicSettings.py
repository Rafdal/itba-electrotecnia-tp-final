from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt
from .slider import Slider
from decimal import Decimal
import numpy as np

class DynamicSettings(QWidget):
    def __init__(self, settings_dict, onValueChanged=lambda k,v: None):
        super().__init__()
        self.settings_dict = settings_dict
        self.sliders = {}
        self.labels = {}
        self.textboxes = {}
        self.onValueChanged = onValueChanged
        self.vlayout = QVBoxLayout()
        self.setLayout(self.vlayout)
        self.initUI()

    def initUI(self):
        self.update(self.settings_dict)

    def update(self, settings_dict):
        self.settings_dict = settings_dict
        while self.vlayout.count():
            child = self.vlayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            if child.layout():
                while child.layout().count():
                    grandchild = child.layout().takeAt(0)
                    if grandchild.widget():
                        grandchild.widget().deleteLater()

        for key, param in self.settings_dict.items():
            slider = Slider(param.min, param.max)

            slider.value_changed.connect(lambda value, key=key: self.sliderCallback(key, value))
            
            textbox = QLineEdit(str(param.value))
            textbox.setMaximumWidth(150)
            textbox.returnPressed.connect(lambda key=key: self.updateParamFromTextbox(key))
            textbox.setAlignment(Qt.AlignmentFlag.AlignLeft)

            label = QLabel(f"{param.name} ({param.unit}) = ")
            label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            label.setFixedWidth(label.sizeHint().width())
            hbox = QHBoxLayout()
            hbox.addWidget(label)
            hbox.addWidget(textbox)
            hbox.setAlignment(Qt.AlignmentFlag.AlignLeft)

            self.vlayout.addLayout(hbox)
            self.vlayout.addWidget(slider)
            self.sliders[key] = slider
            self.textboxes[key] = textbox
            self.labels[key] = label

            self.setSliderInitialPos(key, param.value)

    def sliderCallback(self, key, value):
        if self.settings_dict[key].scale == 'log':
            value = 10 ** value

        self.updateParam(key, value)

    def setSliderInitialPos(self, key, value):
        if self.settings_dict[key].scale == 'log':
            value = np.log10(value)
        self.sliders[key].setValue(value)

    def updateParam(self, key, value):
        # Set param value and Hint Text
        self.settings_dict[key].value = value
        self.onValueChanged(key, value)
        name = self.settings_dict[key].name
        unit = self.settings_dict[key].unit
        self.labels[key].setText(f"{name} ({unit}) = ")
        self.textboxes[key].setText(f"{value:.2f}")

    def updateParamFromTextbox(self, key):
        textbox = self.textboxes[key]
        text = textbox.text()

        try:
            newVal = float(text)
            if self.settings_dict[key].scale == 'log':
                if newVal <= 0.0:
                    newVal = 0.1
                self.sliders[key].setValue(np.log10(newVal))
            else:
                if newVal < self.settings_dict[key].min:
                    newVal = self.settings_dict[key].min
                elif newVal > self.settings_dict[key].max:
                    newVal = self.settings_dict[key].max
                self.sliders[key].setValue(newVal)
            self.updateParam(key, newVal)
        except ValueError:
            textbox.setText(f"{self.settings_dict[key].value:.2f}")