# Python Dropdown Menu Class using PyQt5 

from PyQt5.QtWidgets import QPushButton, QGraphicsDropShadowEffect, QMenu, QAction
from PyQt5.QtGui import QColor

from .button import Button

class DropMenu(Button):
    def __init__(self, parent=None, options=[{'name': 'Option 1', 'callback': lambda: print('Option 1')}]):
        super(DropMenu, self).__init__(options[0]['name'], parent)
        self.options = options
        self.menu = QMenu(self)
        self.setMenu(self.menu)
        self.create_actions()
        self.selected_option = options[0]  # set the first option as the default selected option
        self.update_selected_option(self.selected_option)

    def create_actions(self):
        for option in self.options:
            action = QAction(option['name'], self)
            action.triggered.connect(lambda _, option=option: self.update_selected_option(option))
            self.menu.addAction(action)

    def update_selected_option(self, option):
        self.selected_option = option
        self.setText(option['name'])
        option['callback']()  # call the option's callback function