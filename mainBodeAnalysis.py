import ltspice
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from utils.plotUtils import *

import os

filepath = os.path.join(os.getcwd(), 'data', '2a_bodes.raw')

data = ltspice.Ltspice(filepath) # Carga el archivo .raw

data.parse() # Analiza el archivo .raw

# get variables names and info
print(data.variables) # Muestra las variables disponibles



frec = data.get_frequency() # Obtiene el vector de tiempo
vin = data.get_data('V(vin)')
der_ideal = data.get_data('V(der_ideal)')
der_real = data.get_data('V(der_real)')
int_ideal = data.get_data('V(int_ideal)')
int_real = data.get_data('V(int_real)')

H = np.divide(der_real, vin)
H1 = np.divide(der_ideal, vin)

# constrain data
# [frec, Zin] = constrainData(start = 0.3, end = 0.85, data=[frec, Zin])

# constrain frec
[frec, H, H1] = constrainFrec(start = 100, end = None, data=[frec, H, H1])


gain, phase = getGainPhase(H)
gain1, phase1 = getGainPhase(H1)

# exportCSV('der_Zin.csv', (frec, gain, phase), ['Frecuencia [Hz]', 'Zin [Ohm]', 'Zin [deg]'])

# Create a figure and two axes
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.semilogx(frec, gain, color='tab:red', label='No ideal', linestyle='-')
ax1.semilogx(frec, gain1, color='tab:red', label='Ideal', linestyle='--')
ax1.tick_params(axis='y', labelcolor='tab:red')
ax1.grid(True, which="both", ls="-", axis="x")
ax1.grid(True, which="both", ls="-", axis="y")
# ax1.yaxis.set_minor_locator(plt.LogLocator(base=10, subs='all', numticks=200))
# ax1.yaxis.set_major_locator(plt.LogLocator(base=10, numticks=50))
# SET TICKS

ax2.semilogx(frec, phase, color='tab:blue', linestyle='-', label='No ideal')
ax2.semilogx(frec, phase1, color='tab:blue', linestyle='--', label='Ideal')
ax2.tick_params(axis='y', labelcolor='tab:blue')
ax2.grid(True, which="major", ls="--", color='black', alpha=1.0)


# Set axis locators
ax1.xaxis.set_minor_locator(plt.LogLocator(base=10, subs='all', numticks=200))
ax1.xaxis.set_major_locator(plt.LogLocator(base=10, numticks=50))

# Set the labels
ax1.set_xlabel('Frecuencia $[Hz]$')
ax1.set_ylabel('Ganancia [dB]', color='tab:red')
# ax1.set_ylabel('Zin Magnitude [$\Omega$]', color='tab:red')
ax2.set_ylabel('Fase $[\degree]$', color='tab:blue')

# Adjust the layout of the plot
fig.tight_layout()

# Show the plot
plt.show()