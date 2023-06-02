# Python Dropdown Menu Class using PyQt5 

from PyQt5.QtWidgets import QPushButton, QGraphicsDropShadowEffect, QMenu, QAction
from PyQt5.QtGui import QColor

from .button import Button

class DropDownMenu(Button):
    def __init__(self, title = "Select", keepTitle = True, onChoose = lambda: None, options=[{'name': 'Option 1', 'callback': lambda: print('Option 1')}]):
        super(DropDownMenu, self).__init__(title)
        self.options = options
        self.onChoose = onChoose
        self.keepTitle = keepTitle
        self.menu = QMenu(self)
        self.setMenu(self.menu)
        self.create_actions()
        self.selected_option = {'name': title, 'callback': lambda: print(title)}
        self.update_selected_option(self.selected_option)

    def create_actions(self):
        for option in self.options:
            action = QAction(option['name'], self)
            action.triggered.connect(lambda _, option=option: self.update_selected_option(option))
            self.menu.addAction(action)

    def update_selected_option(self, option):
        self.selected_option = option
        option['callback']()  # call the option's callback function
        if not self.keepTitle:
            self.setText(option['name'])
        self.onChoose()