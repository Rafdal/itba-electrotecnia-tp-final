import ltspice
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from utils.plotUtils import *
import pandas as pd
import os

power = -2 # set the 10 power variable for scale multiplier
ticks_per_decade = 4 # set the number of ticks per decade
plot1_name = "1" 
plot2_name = "2"
x_axis_name = "x-axis"

filepath = os.path.join(os.getcwd(), 'data', 'x_der_comp_r5k1.csv')


# Read CSV file into pandas dataframe
df = pd.read_csv(filepath)

print(df.head())


# Remove any rows with non-numeric values
df = df.apply(pd.to_numeric, errors='coerce').dropna()

time_offset = df[x_axis_name].values[0]

time = (-time_offset) + df[x_axis_name].values # Obtiene el vector de tiempo
vin = df[plot1_name].values * 2 # Obtiene el vector de corriente en el capacitor
vout = df[plot2_name].values * 2 # Obtiene el vector de corriente en el capacitor

# divide the time vector by 10**power
time = time / (10**power)

# plot data
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(time, vin, label='Vin', color='tab:blue')
ax2.plot(time, vout, label='Vout', color='tab:orange')
ax1.legend(loc='upper left')
ax2.legend(loc='lower right')
ax1.grid(True, which="both", ls="-", axis="both")
ax2.grid(True, which="both", ls="-", axis="both")

ax1.tick_params(axis='y', labelcolor='tab:blue')
ax2.tick_params(axis='y', labelcolor='tab:orange')

# set the x-axis major tick locator
ax1.xaxis.set_major_locator(plt.MultipleLocator(1/ticks_per_decade))
ax1.xaxis.set_minor_locator(plt.MultipleLocator(1/(ticks_per_decade*2)))
ax2.yaxis.set_major_locator(plt.MultipleLocator(0.0025))
# ax1.yaxis.set_minor_locator(plt.MultipleLocator(1))

# format the x-axis tick labels with a power of 10 multiplier and 3 significant figures
format_x = ticker.ScalarFormatter(useMathText=True)
format_y = ticker.ScalarFormatter(useMathText=True)
ax1.xaxis.set_major_formatter(format_x)
ax1.yaxis.set_major_formatter(format_y)
# set the x-axis limits to start from 0
ax1.set_xlim(left=0, right=max(time))

# set the x-axis label with a power of 10 multiplier
ax1.set_xlabel(f'Tiempo $[s]$')
ax1.set_ylabel(f'Tensión $[V]$')

# add a text label showing the scale multiplier
ax1.text(1.07, -0.13, f'$\\cdot 10^{{{power}}}$', transform=plt.gca().transAxes,
        ha='right', va='bottom', fontsize=11)

# ax1.yaxis.set_major_locator(plt.LogLocator(base=10, numticks=50))

plt.show()