from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.path import Path
from matplotlib.patches import PathPatch


class RectPlot(QWidget):
    def __init__(self, x, y, title='', logx=False, logy=False, draggable=True):
        super().__init__()

        # Create a figure and add the plot to it
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.plot = self.ax.plot(x, y)[0]

        # Set log scale if requested
        if logx:
            self.ax.set_xscale('log')
        if logy:
            self.ax.set_yscale('log')

        # Add rounded corners to the plot
        self.add_rounded_corners()

        # Set the plot title
        self.ax.set_title(title)

        # Enable dragging and exploration of the plot if requested
        if draggable:
            self.canvas.mpl_connect('button_press_event', self.on_press)
            self.canvas.mpl_connect('button_release_event', self.on_release)
            self.canvas.mpl_connect('motion_notify_event', self.on_motion)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def add_rounded_corners(self):
        # Get the current plot limits
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        # Define the path for the rounded rectangle
        radius = 0.05
        path = Path([
            (xlim[0] + radius, ylim[0]),
            (xlim[1] - radius, ylim[0]),
            (xlim[1], ylim[0] + radius),
            (xlim[1], ylim[1] - radius),
            (xlim[1] - radius, ylim[1]),
            (xlim[0] + radius, ylim[1]),
            (xlim[0], ylim[1] - radius),
            (xlim[0], ylim[0] + radius),
            (xlim[0] + radius, ylim[0]),
        ])
        patch = PathPatch(path, facecolor='none', edgecolor='black', lw=2)

        # Add the rounded rectangle to the plot
        self.ax.add_patch(patch)

    def on_press(self, event):
        self._dragging = True
        self._x0 = event.xdata
        self._y0 = event.ydata

    def on_release(self, event):
        self._dragging = False

    def on_motion(self, event):
        if self._dragging:
            dx = event.xdata - self._x0
            dy = event.ydata - self._y0
            self.ax.set_xlim(self.ax.get_xlim() - dx)
            self.ax.set_ylim(self.ax.get_ylim() - dy)
            self.canvas.draw()