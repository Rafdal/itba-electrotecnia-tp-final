import ltspice
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from utils.plotUtils import *
import pandas as pd
import os

mag_name = "Vr_mag" 
phase_name = "Vr_fase"
freq_name = "Frecuencia"

filepath = os.path.join(os.getcwd(), 'data', 'pasabajo_lab1.csv')


# Read CSV file into pandas dataframe
df = pd.read_csv(filepath)


# Remove any rows with non-numeric values
df = df.apply(pd.to_numeric, errors='coerce').dropna()


frec = df[freq_name].values # Obtiene el vector de tiempo
mag = df[mag_name].values # Obtiene el vector de corriente en el capacitor
phase = df[phase_name].values # Obtiene el vector de corriente en el capacitor
gain = mag

# Create a figure and two axes
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.semilogx(frec, gain, color='tab:red', label='No ideal', linestyle='-')
ax1.tick_params(axis='y', labelcolor='tab:red')
ax1.grid(True, which="both", ls="-", axis="x")
ax1.grid(True, which="both", ls="-", axis="y")
# ax1.yaxis.set_minor_locator(plt.LogLocator(base=10, subs='all', numticks=200))
# ax1.yaxis.set_major_locator(plt.LogLocator(base=10, numticks=50))
# SET TICKS

ax2.semilogx(frec, phase, color='tab:blue', linestyle='-', label='No ideal')
ax2.tick_params(axis='y', labelcolor='tab:blue')
ax2.grid(True, which="major", ls="--", color='black', alpha=1.0)


# Set axis locators
ax1.xaxis.set_minor_locator(plt.LogLocator(base=10, subs='all', numticks=200))
ax1.xaxis.set_major_locator(plt.LogLocator(base=10, numticks=50))

# Set the labels
ax1.set_xlabel('Frecuencia $[Hz]$')
ax1.set_ylabel('Tensión [dB]', color='tab:red')
# ax1.set_ylabel('Zin Magnitude [$\Omega$]', color='tab:red')
ax2.set_ylabel('Fase $[\degree]$', color='tab:blue')

# Adjust the layout of the plot
fig.tight_layout()

# Show the plot
plt.show()