import os
import ltspice
import matplotlib.pyplot as plt
import numpy as np
from libs.LTSpiceReader import ReadLTSpice
from libs.utils import searchMaxMinInRange, mean_spacing

import seaborn as sns
# Define a color palette with 5 colors
# palette = sns.color_palette("hsv", 100)

# Set the color palette
# sns.set_palette(palette)

# FILE INDEX TO OPEN
# No especificar el indice para que pregunte
data = ReadLTSpice(folder="data", idx=None)
data.info() # Imprime información del archivo LTSpice (variables, casos, etc)

plot_VL_C1 = [1, 6]
# plot_VL_C1 = [1, 3]
plot_Altium = [3]

fig, ax1 = plt.subplots()
ax2 = None


montecarloHist = []

if data.l._mode == "AC":
    for i in plot_Altium:
        print(f"Plotting {data.varListNames[i]}")
        symbol = data.varListInfo[i]["symbol"]
        print(f"Symbol: {symbol}")
        c = data.colors[symbol]

        label = data.varListNames[i].upper()

        if data.is_montecarlo:

            for j, run in enumerate(data.varListData[i]):
                if j == 0:
                    showLabel = label
                else:
                    showLabel = None
                dB = 20 * np.log10(np.abs(run))
                phase = np.angle(run, deg=True)

                ax1.semilogx(data.x, dB, linewidth=0.2, alpha=1.0, label=showLabel)
                maxs, mins = searchMaxMinInRange(data.x, dB, 142, 600, c='black', s=3, ax=ax1, returnAxis='y', text = None)
                montecarloHist.append(maxs[0])
    

else:
    for i in plot_VL_C1:
        print(f"Plotting {data.varListNames[i]}")
        symbol = data.varListInfo[i]["symbol"]
        print(f"Symbol: {symbol}")
        c = data.colors[symbol]

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
                    ax2.plot(data.x, run, linewidth=1.0, c=c, alpha=0.4, label=showLabel)
                    # maxs, mins = searchMaxMinInRange(data.x, run, 0.34, 0.36, c='black', s=3, ax=ax2, returnAxis='y', text = None)
                    # if mins[0] < -0.100:

                else:
                    ax1.plot(data.x, run, linewidth=1.0, c=c, alpha=0.4, label=showLabel)
                    # maxs, mins = searchMaxMinInRange(data.x, run, 0.3501, 0.44, c='black', s=3, ax=ax1, returnAxis='x', text = None)
                    # lst = maxs + mins
                    # T = mean_spacing(lst) * 2.0
                    # h = 1.0 / T
                    # if j == 0:
                    #     print(f"Mean spacing: {h}, List: {lst}")
                    # montecarloHist.append(h)
        
        # NOT MONTECARLO
        else:
            x = data.x
            y = data.varListData[i]
            if data.varListInfo[i]["symbol"] == "I":
                ax2 = ax1.twinx()
                # [0:40]
                ax2.plot(x, y, linewidth=1.0, c=c, alpha=1.0, label=label)
                _, mins = searchMaxMinInRange(x, y, 0.04, 0.08, returnAxis='y', ax=ax2, c=c, text = "down", ignore = None)
            else:
                ax1.plot(x, y, linewidth=1.0, c=c, alpha=1.0, label=label)
                _, mins = searchMaxMinInRange(x, y, 0.04, 0.08, returnAxis='y', ignore = None, ax=ax1, c=c, text = "up")


if ax2 is not None:
    ax2.set_ylabel("Current (A)")  # Set the ylabel only if ax2 has been defined
ax1.set_ylabel("Voltage (V)")
ax1.set_xlabel('Time (s)')
ax1.set_title(data.filename)
ax1.grid()
if ax2 is not None:
    ax2.legend(loc="lower right")  # Set the legend only if ax2 has been defined
ax1.legend(loc="upper right")

fig.subplots_adjust(right=0.85) # Adjust the right margin



# Plot histogram
if len(montecarloHist) > 0:
    fig, ax = plt.subplots()
    ax.hist(montecarloHist, bins=25)
    ax.set_xlabel("X Label")
    ax.set_title(data.filename)
    
    
plt.show()