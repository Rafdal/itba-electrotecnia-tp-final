from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor, QPalette
from widgets.button import Button
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QEvent, QPropertyAnimation, QEasingCurve

class MyFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setHoverStyle("#FFFFFF")

        # Install event filter
        self.installEventFilter(self)

    def setHoverStyle(self, color):
        # Set frame properties
        self.setLineWidth(2)
        self.setMidLineWidth(0)
        self.setContentsMargins(8, 8, 8, 8)
        self.setStyleSheet(f"QFrame {{border-radius: 8px; background-color: {color}; }}")
        self.setFixedHeight(40)

        # Add drop shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 127))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)

    def eventFilter(self, obj, event):
        if event.type() == 10:
            self.setHoverStyle("lightblue")
        elif event.type() == 11:
            self.setHoverStyle("#FFFFFF")
        return super().eventFilter(obj, event)



class DynamicWidgetList(QWidget):
    def __init__(self, objects, on_click_callback, on_delete_callback):
        super().__init__()
        self.objects = objects
        self.on_click_callback = on_click_callback
        self.on_delete_callback = on_delete_callback

        self.vlayout = QVBoxLayout()
        self.vlayout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinAndMaxSize)
        self.mainlayout = QVBoxLayout()

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setMinimumHeight(100)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidget(QWidget())
        self.scroll.widget().setLayout(self.vlayout)

        self.mainlayout.addWidget(self.scroll)
        self.setLayout(self.mainlayout)

        self.render_widgets()


    def render_widgets(self):

        for i in reversed(range(self.vlayout.count())):
            self.vlayout.itemAt(i).widget().setParent(None) # type: ignore
        for i in range(len(self.objects)):
            obj = self.objects[i]
            frame = MyFrame()

            # shadow = QGraphicsDropShadowEffect()
            # shadow.setBlurRadius(10)
            # shadow.setColor(QColor(0, 0, 0, 127))
            # shadow.setOffset(0, 0)

            # frame.setGraphicsEffect(shadow)

            row_layout = QHBoxLayout()
            name_label = QLabel(obj.name)
            row_layout.addWidget(name_label)
            row_layout.addStretch(1)
            delete_button = Button("X", hover_color="#ff694b ", background_color="#fff0ed ",on_click=lambda idx=i, name=obj.name: self.on_delete_callback(idx, name))
            delete_button.setMinimumWidth(40)

            row_layout.addWidget(delete_button)
            row_layout.setContentsMargins(0, 0, 0, 0)
            frame.setLayout(row_layout)
            name_label.mousePressEvent = lambda ev, idx=i, name=obj.name: self.on_click_callback(idx, name)
            frame.mousePressEvent = lambda a0, idx=i, name=obj.name: self.on_click_callback(idx, name)
            
            self.vlayout.addWidget(frame)