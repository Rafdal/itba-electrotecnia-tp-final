import ltspice
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from utils.plotUtils import *

import os

filepath = os.path.join(os.getcwd(), 'data', '3_integ_rect.raw')

data = ltspice.Ltspice(filepath) # Carga el archivo .raw

data.parse() # Analiza el archivo .raw


time = data.get_time() # Obtiene el vector de tiempo
vin = data.get_data('V(vin)') # Obtiene el vector de corriente en el capacitor
vout = data.get_data('V(vout)') # Obtiene el vector de corriente en el capacitor

# plot data
plt.plot(time, vin, label='Vin')
plt.plot(time, vout, label='Vout')
plt.legend()
plt.grid(True, which="both", ls="-", axis="both")

# set the x-axis major tick locator
plt.gca().yaxis.set_major_locator(plt.MultipleLocator(1))

# ax1.yaxis.set_minor_locator(plt.LogLocator(base=10, subs='all', numticks=200))
# ax1.yaxis.set_major_locator(plt.LogLocator(base=10, numticks=50))

plt.show()