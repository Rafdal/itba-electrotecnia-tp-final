import ltspice
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from utils.plotUtils import *
import pandas as pd
import os

power = -5 # set the 10 power variable for scale multiplier
ticks_per_decade = 4 # set the number of ticks per decade
plot1_name = "1" 
plot2_name = "2"
x_axis_name = "x-axis"

filepath = os.path.join(os.getcwd(), 'data', '6_int_comp_r5k1_.csv')


# Read CSV file into pandas dataframe
df = pd.read_csv(filepath)

print(df.head())


# Remove any rows with non-numeric values
df = df.apply(pd.to_numeric, errors='coerce').dropna()

time_offset = df[x_axis_name].values[0]

time = (-time_offset) + df[x_axis_name].values # Obtiene el vector de tiempo
vin = df[plot1_name].values # Obtiene el vector de corriente en el capacitor
vout = df[plot2_name].values # Obtiene el vector de corriente en el capacitor

# divide the time vector by 10**power
time = time / (10**power)

# plot data
plt.plot(time, vin, label='Vin')
plt.plot(time, vout, label='Vout')
plt.legend()
plt.grid(True, which="both", ls="-", axis="both")

# set the x-axis major tick locator
plt.gca().yaxis.set_major_locator(plt.MultipleLocator(1))
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(1/ticks_per_decade))
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
plt.gca().text(1.06, -0.08, f'$\\cdot 10^{{{power}}}$', transform=plt.gca().transAxes,
        ha='right', va='bottom', fontsize=10)

# ax1.yaxis.set_major_locator(plt.LogLocator(base=10, numticks=50))

plt.show()