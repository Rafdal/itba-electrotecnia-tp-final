from PyQt5.QtWidgets import QLabel, QDialog, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

class PopUpForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Custom Filter Settings')
        self.resize(300, 100)
        self.label1 = QLabel('Polinomio Numerador')
        self.textbox1 = QLineEdit(self)
        self.textbox1.setPlaceholderText('ej: 3*s**2 + 2*s + 1500')
        self.label2 = QLabel('Polinomio Denominador')
        self.textbox2 = QLineEdit(self)
        self.textbox2.setPlaceholderText('ej: 0.6*s**2 - 0.2*s + 2300')
        self.button = QPushButton('Submit', self)
        self.button.clicked.connect(self.submit)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label1)
        layout.addWidget(self.textbox1)
        layout.addWidget(self.label2)
        layout.addWidget(self.textbox2)
        layout.addWidget(self.button)

    def submit(self):
        try:
            text1 = self.textbox1.text()
            text2 = self.textbox2.text()
            self.callback(text1, text2)
        except Exception as e:
            print("DOMADO:", e)
            # show a dialog with the error
            QMessageBox.critical(self, 'Error', str(e))
        else:
            self.accept()

    def set_callback(self, callback):
        self.callback = callback
