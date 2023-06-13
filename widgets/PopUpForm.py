from PyQt5.QtWidgets import QLabel, QDialog, QLineEdit, QPushButton, QVBoxLayout

class PopUpForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('PopUp Form')
        self.resize(300, 100)
        self.label1 = QLabel('Text1')
        self.textbox1 = QLineEdit(self)
        self.label2 = QLabel('Text2')
        self.textbox2 = QLineEdit(self)
        self.button = QPushButton('Submit', self)
        self.button.clicked.connect(self.submit)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label1)
        layout.addWidget(self.textbox1)
        layout.addWidget(self.label2)
        layout.addWidget(self.textbox2)
        layout.addWidget(self.button)

    def submit(self):
        text1 = self.textbox1.text()
        text2 = self.textbox2.text()
        self.accept()
        self.callback(text1, text2)

    def set_callback(self, callback):
        self.callback = callback

from PyQt5.QtWidgets import QApplication
if __name__ == '__main__':
    app = QApplication([])
    form = PopUpForm()
    form.set_callback(lambda text1, text2: print(f'Text1: {text1}, Text2: {text2}'))
    button = QPushButton('Show Form')
    button.clicked.connect(form.show)
    layout = QVBoxLayout()
    layout.addWidget(button)
    widget = QDialog()
    widget.setLayout(layout)
    widget.show()
    app.exec_() 
