from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter
from matplotlib import rcParams
import numpy as np
from PyQt5.QtCore import Qt
import math

class RectPlotBase(QWidget):
    def __init__(self, draggable=True, scale='linear', postFix=None, yInitRange=20.0):
        super().__init__()

        # Create a figure and add the plot to it
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        # Set the margins and padding of the subplot
        self.figure.subplots_adjust(top=1.0, right=0.99)
        self.ax = self.figure.add_subplot(111)

        self.yInitRange = yInitRange

        self._dragging = False

        if scale == 'linear':
            pass
        elif scale == 'log10':
            self.ax.xaxis.set_major_formatter(FuncFormatter(self.format_log10))
        elif scale == 'log2':
            self.ax.xaxis.set_major_formatter(FuncFormatter(self.format_log2))
        else:
            raise ValueError(f'Invalid scale: {scale}')
        
        if postFix != None:
            self.ax.yaxis.set_major_formatter(FuncFormatter(lambda y, t: f'{y:.2f}{postFix}'))

        # add log grid
        self.ax.grid(True, which='major', axis='both', linestyle='--', linewidth=0.5)

        # Enable dragging and exploration of the plot if requested
        if draggable:
            self.canvas.mpl_connect('button_press_event', self.on_press)
            self.canvas.mpl_connect('button_release_event', self.on_release)
            self.canvas.mpl_connect('motion_notify_event', self.on_motion)
            self.canvas.mpl_connect('scroll_event', self.on_scroll)

        # Set up the layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.canvas)
        layout.setStretch(0, 1)  # Set the vertical stretch factor to 1
        self.setLayout(layout)

    # Format x-axis tick labels in log scale
    def format_log10(self, exp, tick_number):
        coeff = (10**(exp - int(exp)))
        return f'${coeff:.1f} \\times 10^{{{int(exp)}}}$'
    
    def format_log2(self, exp, tick_number):
        coeff = (2**(exp - int(exp)))
        return f'${coeff:.1f} \\times 2^{{{int(exp)}}}$'

    def on_press(self, event):
        self._dragging = True
        self._x0 = event.xdata
        self._y0 = event.ydata

    def on_release(self, event):
        self._dragging = False

    def init_plot(self, x, yList):
        for y in yList:
            self.plot = self.ax.plot(x, y)[0]
        
        # check y limits range
        y_range = self.ax.get_ylim()[1] - self.ax.get_ylim()[0]
        if y_range < self.yInitRange:
            # set y limits vertically centered to the plot with range of 20
            y_center = (self.ax.get_ylim()[0] + self.ax.get_ylim()[1]) / 2.0
            self.ax.set_ylim(y_center - self.yInitRange/2.0, y_center + self.yInitRange/2.0)

        # save initial limits
        self.initial_xlim = self.ax.get_xlim()
        self.initial_ylim = self.ax.get_ylim()

        # redraw plot
        self.canvas.draw()

    def update_plot(self, x, yList):
        for i, y in enumerate(yList):
            if i < len(self.ax.lines):
                self.ax.lines[i].set_ydata(y)
            else:
                self.ax.plot(x, y)
        self.canvas.draw_idle()

    def on_motion(self, event):
        if event is None:
            return
        if event.xdata is None or event.ydata is None:
            return
        if not self._dragging:
            return
    
        dx = event.xdata - self._x0
        dy = event.ydata - self._y0

        self.ax.set_xlim(self.ax.get_xlim() - dx)
        self.ax.set_ylim(self.ax.get_ylim() - dy)
        self.canvas.draw_idle()

    def on_scroll(self, event):
        if event.button == 'up':
            # Zoom in
            scale_factor = 1 / 1.2

        elif event.button == 'down':
            # Zoom out
            scale_factor = 1.2
        else:
            # Ignore other buttons
            return

        x_range = self.ax.get_xlim()
        y_range = self.ax.get_ylim()

        x_center = (x_range[0] + x_range[1]) / 2
        y_center = (y_range[0] + y_range[1]) / 2

        x_new_range = (x_range[0] - x_center) * scale_factor + x_center, (x_range[1] - x_center) * scale_factor + x_center
        y_new_range = (y_range[0] - y_center) * scale_factor + y_center, (y_range[1] - y_center) * scale_factor + y_center

        self.ax.set_xlim(x_new_range[0], x_new_range[1])
        self.ax.set_ylim(y_new_range[0], y_new_range[1])
        self.canvas.draw_idle()

    def reset_plot(self):
        print('resetting plot')
        # Reset the plot to the initial parameters
        self.ax.set_xlim(self.initial_xlim[0], self.initial_xlim[1])
        self.ax.set_ylim(self.initial_ylim[0], self.initial_ylim[1])

        self.canvas.draw_idle()

    def autoscale_x(self):
        # Get the x data from the plot
        x_data = []
        for line in self.ax.lines:
            x_data.extend(line.get_xdata())

        # Set the x axis limits based on the data range
        if x_data:
            x_range = max(x_data) - min(x_data)
            x_margin = x_range * 0.02
            self.ax.set_xlim(min(x_data) - x_margin, max(x_data) + x_margin)

        # Redraw the canvas
        self.canvas.draw_idle()

    def autoscale_y(self):
        # Get the y data from the plot
        y_data = []
        for line in self.ax.lines:
            y_data.extend(line.get_ydata())

        # Set the y axis limits based on the data range
        if y_data:
            # remove Inf or NaN
            y_data = [y for y in y_data if not math.isnan(y) and not math.isinf(y)]
            if(len(y_data) >= 5):
                y_min = min(y_data)
                y_max = max(y_data)
                y_range = y_max - y_min
                y_margin = y_range * 0.1
                self.ax.set_ylim(y_min - y_margin, y_max + y_margin)

        # Redraw the canvas
        self.canvas.draw_idle()

    def center_plot(self):
        print('centering plot')

        # Calculate the initial center point
        x_center = (self.initial_xlim[0] + self.initial_xlim[1]) / 2
        y_center = (self.initial_ylim[0] + self.initial_ylim[1]) / 2

        # Get the current x and y limits
        x_range = self.ax.get_xlim()
        y_range = self.ax.get_ylim()

        # Calculate the current zoom
        x_zoom = (x_range[1] - x_range[0]) / (self.initial_xlim[1] - self.initial_xlim[0])
        y_zoom = (y_range[1] - y_range[0]) / (self.initial_ylim[1] - self.initial_ylim[0])

        # Calculate the new x and y limits to be centered around the initial center point
        x_new_range = x_center - (self.initial_xlim[1] - self.initial_xlim[0]) / 2 * x_zoom, x_center + (self.initial_xlim[1] - self.initial_xlim[0]) / 2 * x_zoom
        y_new_range = y_center - (self.initial_ylim[1] - self.initial_ylim[0]) / 2 * y_zoom, y_center + (self.initial_ylim[1] - self.initial_ylim[0]) / 2 * y_zoom
    
        # Set the new x and y limits
        self.ax.set_xlim(x_new_range[0], x_new_range[1])
        self.ax.set_ylim(y_new_range[0], y_new_range[1])

        self.canvas.draw_idle()