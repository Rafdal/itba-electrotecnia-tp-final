import ltspice
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from utils.plotUtils import *
import pandas as pd
import os

power = -5 # set the 10 power variable for scale multiplier
plot1_name = "1" 
plot2_name = "2"

filepath = os.path.join(os.getcwd(), 'data', 'der_pk2.csv')


# Read CSV file into pandas dataframe
df = pd.read_csv(filepath)

# Remove any rows with non-numeric values
df = df.apply(pd.to_numeric, errors='coerce').dropna()

time_offset = df["x-axis"].values[0]

time = -time_offset + df["x-axis"].values # Obtiene el vector de tiempo
vin = df["1"].values # Obtiene el vector de corriente en el capacitor
vout = df["2"].values # Obtiene el vector de corriente en el capacitor

# divide the time vector by 10**power
time = time / (10**power)

# plot data
plt.plot(time, vin, label='Vin')
plt.plot(time, vout, label='Vout')
plt.legend()
plt.grid(True, which="both", ls="-", axis="both")

# set the x-axis major tick locator
plt.gca().yaxis.set_major_locator(plt.MultipleLocator(2))
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(2))

# format the x-axis tick labels with a power of 10 multiplier and 3 significant figures
format_x = ticker.EngFormatter(places=0, sep=u"\N{THIN SPACE}", usetex=True)
plt.gca().xaxis.set_major_formatter(format_x)
format_y = ticker.EngFormatter(places=0, sep=u"\N{THIN SPACE}", usetex=True)
plt.gca().yaxis.set_major_formatter(format_y)

# set the x-axis label with a power of 10 multiplier
plt.gca().set_xlabel(f'Tiempo $[s]$')
plt.gca().set_ylabel(f'Tensión $[V]$')

# add a text label showing the scale multiplier
plt.gca().text(1.07, -0.1, f'$\\cdot 10^{{{power}}}$', transform=plt.gca().transAxes,
        ha='right', va='bottom', fontsize=10)

# ax1.yaxis.set_minor_locator(plt.LogLocator(base=10, subs='all', numticks=200))
# ax1.yaxis.set_major_locator(plt.LogLocator(base=10, numticks=50))

plt.show()