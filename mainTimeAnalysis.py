import ltspice
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from utils.plotUtils import *

import os

filepath = os.path.join(os.getcwd(), 'data', '3_int_cuad_sim.raw')

power = -4 # set the 10 power variable for scale multiplier
ticks_per_decade = 1 # set the number of ticks per unit
minor_ticks_between = 3

data = ltspice.Ltspice(filepath) # Carga el archivo .raw

data.parse() # Analiza el archivo .raw


time = data.get_time() # Obtiene el vector de tiempo
vin = data.get_data('V(vin)') # Obtiene el vector de corriente en el capacitor
vout = data.get_data('V(vout)') # Obtiene el vector de corriente en el capacitor

#constraint data
[time, vin, vout] = constrainData(start = 0.94, end = 1.0, data=[time, vin, vout])

time = time - time[0]

# divide the time vector by 10**power
time = time / (10**power)

# plot data
plt.plot(time, vin, label='Vin')
plt.plot(time, vout, label='Vout')
plt.legend()
plt.grid(True, which="both", ls="-", axis="both")

# set the x-axis major tick locator
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(1/ticks_per_decade))
plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(1/(ticks_per_decade*(minor_ticks_between+1))))
plt.gca().yaxis.set_major_locator(plt.MultipleLocator(2))
plt.gca().yaxis.set_minor_locator(plt.MultipleLocator(1))

# format the x-axis tick labels with a power of 10 multiplier and 3 significant figures
format_x = ticker.ScalarFormatter(useMathText=True)
format_y = ticker.ScalarFormatter(useMathText=True)
plt.gca().xaxis.set_major_formatter(format_x)
plt.gca().yaxis.set_major_formatter(format_y)
# set the x-axis limits to start from 0
plt.gca().set_xlim(left=0, right=max(time))

# set the x-axis label with a power of 10 multiplier
plt.gca().set_xlabel(f'Tiempo $[s]$')
plt.gca().set_ylabel(f'Tensión $[V]$')

# add a text label showing the scale multiplier
plt.gca().text(1.06, -0.12, f'$\\cdot 10^{{{power}}}$', transform=plt.gca().transAxes,
        ha='right', va='bottom', fontsize=12)

# ax1.yaxis.set_major_locator(plt.LogLocator(base=10, numticks=50))

plt.show()