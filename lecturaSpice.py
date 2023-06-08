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

fig, ax1 = plt.subplots()

for i in plot_VL_C1:
    print(f"Plotting {data.varListNames[i]}")
    symbol = data.varListInfo[i]["symbol"]
    print(f"Symbol: {symbol}")
    color = data.colors[symbol]
    if data.is_montecarlo:
        for run in data.varListData[i]:
            ax1.plot(data.time, run, linewidth=0.5, color=color, alpha=0.2)
    else:
        if data.varListInfo[i]["symbol"] == "I":
            ax2 = ax1.twinx()
            ax2.set_ylabel("Voltage (V)")
            ax2.plot(data.time, data.varListData[i], linewidth=1.0, color=color, alpha=1.0, label=data.varListNames[i])
        else:
            ax1.plot(data.time, data.varListData[i], linewidth=1.0, color=color, alpha=1.0, label=data.varListNames[i])


ax1.set_ylabel("Current (A)")
ax1.set_xlabel('Time (s)')
ax1.grid()
ax1.legend()
plt.show()