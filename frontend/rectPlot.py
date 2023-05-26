from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter
from matplotlib import rcParams
import numpy as np

class RectPlot(QWidget):
    def __init__(self, x, y, title='', draggable=True, scale='linear', db=False):
        super().__init__()

        # Create a figure and add the plot to it
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.plot = self.ax.plot(x, y)[0]
        self._dragging = False

        # Save the initial plot parameters
        self.initial_xlim = self.ax.get_xlim()
        self.initial_ylim = self.ax.get_ylim()

        # Enable LaTeX rendering
        rcParams['text.usetex'] = True

        if scale == 'linear':
            pass
        elif scale == 'log10':
            self.ax.xaxis.set_major_formatter(FuncFormatter(self.format_log10))
        elif scale == 'log2':
            self.ax.xaxis.set_major_formatter(FuncFormatter(self.format_log2))
        else:
            raise ValueError(f'Invalid scale: {scale}')
        
        if db:
            self.ax.yaxis.set_major_formatter(FuncFormatter(lambda y, t: f'{y}dB'))

        # Set the plot title
        self.ax.set_title(title)

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
        layout.addWidget(self.canvas)
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

    def update_plot(self, x, y):
        self.plot.set_data(x, y)
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

    def autoscale_plot(self):
        print('autoscaling plot')
        # Get the x and y data from the plot
        x_data, y_data = [], []
        for line in self.ax.lines:
            x_data.extend(line.get_xdata())
            y_data.extend(line.get_ydata())

        # Set the plot limits based on the data range
        if x_data:
            x_range = max(x_data) - min(x_data)
            x_margin = x_range * 0.05
            self.ax.set_xlim(min(x_data) - x_margin, max(x_data) + x_margin)
        if y_data:
            y_range = max(y_data) - min(y_data)
            y_margin = y_range * 0.05
            self.ax.set_ylim(min(y_data) - y_margin, max(y_data) + y_margin)

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