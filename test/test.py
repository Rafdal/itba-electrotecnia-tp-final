from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QVBoxLayout
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor

app = QApplication([])
window = QWidget()

# Create a QFrame with a border and rounded corners
frame = QFrame(window)


# Add the QFrame to the window
layout = QVBoxLayout()
layout.addWidget(frame)
window.setLayout(layout)

window.show()
app.exec_()