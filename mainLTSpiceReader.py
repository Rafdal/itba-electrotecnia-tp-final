import ltspice
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from utils.plotUtils import *

import os

filepath = os.path.join(os.getcwd(), 'data', 'Zin2.raw')

data = ltspice.Ltspice(filepath) # Carga el archivo .raw
data.parse() # Analiza el archivo .raw

# get variables names and info
print(data.variables) # Muestra las variables disponibles


frec = data.get_data('frequency')
Vin = data.get_data('V(vin)')
I_in = data.get_data('I(V1)')

Zin = np.divide(Vin, I_in)

# constrain data
# [frec, Zin] = constrainData(start = 0.3, end = 0.85, data=[frec, Zin])

# constrain frec
[frec, Zin] = constrainFrec(start = 1e-1, end = 1e+6, data=[frec, Zin])

mag = np.abs(Zin)
phase = fixPhaseJumps(np.angle(Zin, deg=True))

# Create a figure and two axes
fig, ax1 = plt.subplots()
# ax2 = ax1.twinx()

ax1.loglog(frec, mag, color='tab:red', label='No ideal', linestyle='-')
ax1.tick_params(axis='y', labelcolor='tab:red')
ax1.grid(True, which="both", ls="-", axis="x")
ax1.grid(True, which="both", ls="-", axis="y")
ax1.yaxis.set_major_locator(plt.LogLocator(base=10, subs='all', numticks=200))
ax1.yaxis.set_minor_locator(plt.LogLocator(base=10, subs='all', numticks=200))

# ax1.yaxis.set_major_formatter(ticker.LogFormatterSciNotation(base=10, labelOnlyBase=False))
ax1.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))

# ax2.yaxis.set_major_locator(plt.MultipleLocator(15))
# ax2.semilogx(frec, phase, color='tab:blue', linestyle='-', label='No ideal')
# ax2.tick_params(axis='y', labelcolor='tab:blue')
# ax2.grid(True, which="major", ls="-", alpha=0.6)


# Set axis locators
ax1.xaxis.set_minor_locator(plt.LogLocator(base=10, subs='all', numticks=200))
ax1.xaxis.set_major_locator(plt.LogLocator(base=10, numticks=50))
# ax1.xaxis.set_major_formatter(ticker.EngFormatter(sep=''))
# ax1.xaxis.set_minor_formatter(ticker.EngFormatter(sep=''))

# Set the labels
ax1.set_xlabel('Frecuencia $[Hz]$')
ax1.set_ylabel('$|Z_{{IN}}|$   $[\\Omega]$', color='tab:red')
# ax1.set_ylabel('Zin Magnitude [$\Omega$]', color='tab:red')
# ax2.set_ylabel('Fase  $Z_{{IN}}$  $[\degree]$', color='tab:blue')

# Adjust the layout of the plot
fig.tight_layout()

# Set x axis limits according to frec
ax1.set_xlim([frec[0], frec[-1]])


# Show the plot
plt.show()