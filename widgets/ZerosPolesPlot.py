
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rcParams

from scipy import signal
import numpy as np

class ZerosPolesPlot(QWidget):
    def __init__(self, data):
        super().__init__()
        self.title = "Diagrama de Polos y Ceros"
        self.figure = plt.figure(figsize=(5, 5))
        # self.figure.subplots_adjust(left=0.06, right=1.1, bottom=0.1, top=0.98)
        self.canvas = FigureCanvas(self.figure)  # Create a canvas to display the plot
        self.layout = QVBoxLayout()  # Create a vertical layout to add the canvas to
        self.layout.addWidget(self.canvas)  # Add the canvas to the layout
        self.setLayout(self.layout)  # Set the layout for the widget
        self.setMinimumSize(200, 200)

        self.marginFactor = 1.2



        # set widget aspect ratio
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.data = data

        self.ax = self.figure.add_subplot(111)
        self.figure.patch.set_facecolor((0,0,0,0))
        self.ax.patch.set_facecolor((0,0,0,0))

        # Create some sample data for the scatter plot
        z, p = self.get_plot_data()
        self.init_plot(z, p)

        self.ax.set_aspect('equal')

    def on_tab_focus(self):
        z, p = self.get_plot_data()
        
        # remove old plot and update
        self.ax.clear()
        self.init_plot(z, p)
        pass

    def get_plot_data(self):
        # Get poles and zeros from the transfer function
        Zeros, Poles, Gain = signal.tf2zpk(self.data.F.num, self.data.F.den)
        return Zeros, Poles


    def init_plot(self, zeros, poles):
        self.plot = self.ax.scatter(np.real(zeros), np.imag(zeros), facecolors='white', edgecolors='blue', s=50, label='Zeros')
        self.plot = self.ax.scatter(np.real(poles), np.imag(poles), marker='x', color='red', s=50, label='Poles')

        # Find the max value for the axes to keep the aspect ratio correct
        r = self.marginFactor * np.amax(np.concatenate((abs(poles), abs(zeros), [1])))

        # Set the limits for the plot
        if r < 10.0:
            r = 10.0

        self.ax.set_xlim([-r, r])
        self.ax.set_ylim([-r, r])

        self.draw_custom_grid()

        self.ax.axhline(y=0, color='black', linewidth=0.5, alpha=0.7, zorder=2)
        self.ax.axvline(x=0, color='black', linewidth=0.5, alpha=0.7, zorder=2)


        # redraw plot
        self.canvas.draw()

    # def update_plot(self, zeros, poles):
    #     print("update plot")

    #     # Remove old scatter plots
    #     for plot in self.ax.collections:
    #         plot.remove()

    #     # Add new scatter plots

    #     self.plot = self.ax.scatter(np.real(zeros), np.imag(zeros), facecolors='white', edgecolors='blue', s=50, label='Zeros')
    #     self.plot = self.ax.scatter(np.real(poles), np.imag(poles), marker='x', color='red', s=50, label='Poles')
        
    #     r = self.marginFactor * np.amax(np.concatenate((abs(poles), abs(zeros), [1])))

    #     self.ax.set_xlim([-r, r])
    #     self.ax.set_ylim([-r, r])

    #     self.draw_custom_grid()

    #     self.ax.axhline(y=0, color='black', linewidth=5.0, alpha=1.0, zorder=2)
    #     self.ax.axvline(x=0, color='black', linewidth=5.0, alpha=1.0, zorder=2)

    #     self.canvas.draw_idle()

    def draw_custom_grid(self):
        # Remove old grid lines
        for line in self.ax.lines:
            line.remove()

        # Generate x and y tick values
        x_min, x_max = self.ax.get_xlim()
        y_min, y_max = self.ax.get_ylim()
        x_ticks = np.arange(x_min, x_max, (x_max - x_min) / 5)
        y_ticks = np.arange(y_min, y_max, (y_max - y_min) / 5)

        # Draw custom grid lines
        self.ax.set_xticks(x_ticks, minor=True)
        self.ax.set_yticks(y_ticks, minor=True)
        self.ax.grid(which='major', alpha=0.3)
        # self.ax.grid(which='major', alpha=0.5)

        self.ax.set_title(self.title)
