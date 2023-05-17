
from PyQt5.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor

# Button class

class Button(QPushButton):

    def __init__(self, text, parent=None, color="black", background_color = "white", radius=10,
                        shadow_color="grey", shadow_radius=9, hover_color="lightblue", click_color="grey"):
        super().__init__(text, parent)

        self.setStyleSheet(f"""
            QPushButton {{ 
                color: {color};
                background-color: {background_color};
                border-radius: {radius}px;                
            }}""" +

        f"""
            QPushButton:hover {{
                background-color: {hover_color};
                border-radius: {radius}px;
                padding: 1px;
            }}

            QPushButton:pressed {{
                background-color: {click_color};
                border-radius: {radius}px;
                padding: 1px;
            }}
        """)

        self.clicked.connect(self.on_click)

        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(shadow_color))
        shadow.setOffset(0, 0)
        shadow.setBlurRadius(shadow_radius)
        self.setGraphicsEffect(shadow)

    def on_click(self):
        print("Button clicked!")