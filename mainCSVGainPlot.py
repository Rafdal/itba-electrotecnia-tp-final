import ltspice
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from utils.plotUtils import *
import pandas as pd
import os

filepath = os.path.join(os.getcwd(), 'data', 'lab1_p4.csv')

# Read CSV file into pandas dataframe
df = pd.read_csv(filepath)


# Remove any rows with non-numeric values
df = df.apply(pd.to_numeric, errors='coerce').dropna()


frec = df["f"].values # Obtiene el vector de tiempo
gain = df["g"].values # Obtiene el vector de corriente en el capacitor


# Create a figure and two axes
fig, ax1 = plt.subplots()

ax1.semilogx(frec, gain, color='tab:red', label='No ideal', linestyle='-')
ax1.tick_params(axis='y', labelcolor='tab:red')
ax1.grid(True, which="both", ls="-", axis="x")
ax1.grid(True, which="both", ls="-", axis="y")
# ax1.yaxis.set_minor_locator(plt.LogLocator(base=10, subs='all', numticks=200))
# ax1.yaxis.set_major_locator(plt.LogLocator(base=10, numticks=50))
# SET TICKS


# Set axis locators
ax1.xaxis.set_minor_locator(plt.LogLocator(base=10, subs='all', numticks=200))
ax1.xaxis.set_major_locator(plt.LogLocator(base=10, numticks=50))

# Set the labels
ax1.set_xlabel('Frecuencia $[Hz]$')
ax1.set_ylabel('Ganancia [dB]', color='tab:red')
# ax1.set_ylabel('Zin Magnitude [$\Omega$]', color='tab:red')


# Adjust the layout of the plot
fig.tight_layout()

# Show the plot
plt.show()