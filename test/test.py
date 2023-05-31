from PyQt5 import QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np
import matplotlib.pyplot as plt

data = np.array([[1.36, 0.01],
[1.4,0.02],
[1.45,0.06],
[1.5,0.17],
[1.6,0.152],
[1.7,1.9],
[1.74,3.8],
[1.76,5.7],
[1.78,7.6],
[1.79,9.5],
[1.81,11.4],
[1.82,13.3],
[1.83,15.2],
[1.84,17.1],
[1.85,19],
[1.86,20.9],
[1.87,22.8],
[1.88,24.7],
[1.88,26.6],
[1.89,28.5]])

data2 = np.array([
[2.59,	1.693],
[2.67, 3.386],
[2.72, 5.079],
[2.77, 6.772],
[2.8, 8.465],
[2.82, 10.158],
[2.85, 11.851],
[2.88, 13.544],
[2.9, 15.237],
[2.92, 16.93],
[2.94, 18.623],
[2.96, 20.316],
[2.98, 22.009],
[3, 23.702],
[3.02, 25.395],
[3.04, 25.4],])

x = data2[:,0]
y = data2[:,1]

# compute a linear regression
x_lin = x[:]
y_lin = y[:]
A = np.vstack([x_lin, np.ones(len(x_lin))]).T
m, c = np.linalg.lstsq(A, y_lin, rcond=None)[0]
print("Line Solution is y = {m}x + {c}".format(m=m,c=c))

# calculate regression values
y_reg = 59.246*x - 155.53

fig = Figure()
canvas = FigureCanvas(fig)

# Plot the data
ax = fig.add_subplot(111)
ax.plot(x, y, color='blue', alpha=0.4, linewidth=2.5, linestyle='-')
ax.plot(x, y_reg, color='red')
ax.scatter(x, y, alpha=1.0)
ax.grid(True)

ax.set_title('Led Verde')
ax.set_xlabel('Tensión [V]')
ax.set_ylabel('Corriente [mA]')
ax.set_ylim(-1, np.max(y)*1.1)

# Draw the canvas
canvas.draw()

# Copy the plot to the clipboard
pixmap = QtGui.QPixmap(canvas.size())
canvas.render(pixmap)
QtGui.QGuiApplication.clipboard().setPixmap(pixmap)