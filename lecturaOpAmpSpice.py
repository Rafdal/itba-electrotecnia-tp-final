import os
import ltspice
import matplotlib.pyplot as plt
import numpy as np
from libs.LTSpiceReader import ReadLTSpice
from libs.utils import searchMaxMinInRange, mean_spacing

# FILE INDEX TO OPEN
# No especificar el indice para que pregunte
data = ReadLTSpice(folder="data", idx=1)

l = data.l

for i in range(l.case_count):
    f = l.get_frequency()
    Vout = l.get_data('V(n002)', i)
    Vout_amp = 20 * np.log10(np.abs(Vout))
    plt.semilogx(f, Vout_amp, label=f'Vout {i}')

plt.show()