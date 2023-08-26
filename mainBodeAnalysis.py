import ltspice
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from utils.plotUtils import *

import os

filepath = os.path.join(os.getcwd(), 'data', 'Pt4_simulacion.raw')

data = ltspice.Ltspice(filepath) # Carga el archivo .raw
data.parse() # Analiza el archivo .raw

# get variables names and info
print(data.variables) # Muestra las variables disponibles

# frec = []
# vin1 = []
# vin2 = []
# vout = []

# for i in range(len(data.case_count)):
#     frec.append(data.get_data('frequency', i))
#     vin1.append(data.get_data('V(v1)', i))
#     vin2.append(data.get_data('V(v2)', i))
#     vout.append(data.get_data('V(vout)', i))

frec = data.get_data('frequency', 0)
vin = data.get_data('V(vin)', 0)
vout = data.get_data('V(vout)', 0)

H = np.divide(vout, vin)

# H1 = np.divide(der_ideal, vin)

# constrain data
# [frec, Zin] = constrainData(start = 0.3, end = 0.85, data=[frec, Zin])

# constrain frec
[frec, H] = constrainFrec(start = 100, end = None, data=[frec, H])


gain, phase = getGainPhase(H)
# gain1, phase1 = getGainPhase(H1)

# exportCSV('der_Zin.csv', (frec, gain, phase), ['Frecuencia [Hz]', 'Zin [Ohm]', 'Zin [deg]'])


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
ax1.set_ylabel('Ganancia [dB]', color='tab:red')
# ax1.set_ylabel('Zin Magnitude [$\Omega$]', color='tab:red')
ax2.set_ylabel('Fase $[\degree]$', color='tab:blue')

# Adjust the layout of the plot
fig.tight_layout()

# Show the plot
plt.show()