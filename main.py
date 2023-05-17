import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

# include button class
from frontend.button import Button

class ExampleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Example App')
        self.setGeometry(100, 100, 500, 400)

        label = QLabel('Hello, PyQt5!', self)
        label.move(150, 150)

        button = Button("Click Me!", self)
        button.move(200, 200)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ExampleApp()
    sys.exit(app.exec_())
