import os
import ltspice
import matplotlib.pyplot as plt
import numpy as np
from libs.LTSpiceReader import ReadLTSpice
from libs.utils import searchMaxMinInRange, mean_spacing

# FILE INDEX TO OPEN
# No especificar el indice para que pregunte
data = ReadLTSpice(folder="data", idx=None)
data.info() # Imprime información del archivo LTSpice (variables, casos, etc)

plot_VL_C1 = [0, 4]
# plot_VL_C1 = [1, 3]



fig, ax1 = plt.subplots()
ax2 = None


montecarloHist = []

for i in plot_VL_C1:
    print(f"Plotting {data.varListNames[i]}")
    symbol = data.varListInfo[i]["symbol"]
    print(f"Symbol: {symbol}")
    color = data.colors[symbol]

    label = data.varListNames[i].upper()

    if data.is_montecarlo:
        if ax2 == None:
            ax2 = ax1.twinx()

        for j, run in enumerate(data.varListData[i]):
            if j == 0:
                showLabel = label
            else:
                showLabel = None
            if data.varListInfo[i]["symbol"] == "I":
                ax2.plot(data.time, run, linewidth=1.0, color=color, alpha=0.4, label=showLabel)
                # maxs, mins = searchMaxMinInRange(data.time, run, 0.005, 0.02, ax=ax2, axisFlag='y', text = None, c=color)

            else:
                ax1.plot(data.time, run, linewidth=1.0, color=color, alpha=0.4, label=showLabel)
                maxs, mins = searchMaxMinInRange(data.time, run, 0.005, 0.06, ax=ax1, axisFlag='x', text = None, c=color)
                lst = maxs + mins
                T = mean_spacing(lst) * 2.0
                h = 1.0 / T
                if j == 0:
                    print(f"Mean spacing: {h}, List: {lst}")
                montecarloHist.append(h)
    
    # NOT MONTECARLO
    else:
        if data.varListInfo[i]["symbol"] == "I":
            ax2 = ax1.twinx()
            # [0:40]
            ax2.plot(data.time, data.varListData[i], linewidth=1.0, color=color, alpha=1.0, label=label)
            # searchMaxMinInRange(data.time, data.varListData[i], 0.0, 0.005, ax=ax2, text = "down")
        else:
            ax1.plot(data.time, data.varListData[i], linewidth=1.0, color=color, alpha=1.0, label=label)
            # searchMaxMinInRange(data.time, data.varListData[i], 0.005, 0.060, ax=ax1, text = "up")


if ax2 is not None:
    ax2.set_ylabel("Current (A)")  # Set the ylabel only if ax2 has been defined
ax1.set_ylabel("Voltage (V)")
ax1.set_xlabel('Time (s)')
ax1.grid()
if ax2 is not None:
    ax2.legend(loc="lower right")  # Set the legend only if ax2 has been defined
ax1.legend(loc="upper right")

fig.subplots_adjust(right=0.85) # Adjust the right margin



# Plot histogram
if len(montecarloHist) > 0:
    fig, ax = plt.subplots()
    ax.hist(montecarloHist, bins=7)
    ax.set_ylabel("Frequency")
    ax.set_title("Histogram")
    
    
plt.show()