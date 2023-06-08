import os
import ltspice
import matplotlib.pyplot as plt
import numpy as np
from backend.LTSpiceReader import ReadLTSpice

# FILE INDEX TO OPEN
# No especificar el indice para que pregunte
data = ReadLTSpice(folder="data", idx=0)
data.info() # Imprime información del archivo LTSpice (variables, casos, etc)

plot_VL_C1 = [0, 4]

print(len(data.varListInfo))

for i in plot_VL_C1:

    print(f"Plotting {data.varListNames[i]}")

    symbol = data.varListInfo[i]["symbol"]
    print(f"Symbol: {symbol}")
    color = data.colors[symbol]
    if data.is_montecarlo:
        for run in data.varListData[i]:
            plt.plot(data.time, run, linewidth=0.5, color=color, alpha=0.2)

    else:
        plt.plot(data.time, data.varListData[i], linewidth=1.0, color=color, alpha=1.0, label=data.varListNames[i])

plt.ylabel("Current (A)")
plt.xlabel('Time (s)')
plt.grid()
plt.legend()
plt.show()