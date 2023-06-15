import os
import ltspice
import matplotlib.pyplot as plt
import numpy as np
from libs.LTSpiceReader import ReadLTSpice

# FILE INDEX TO OPEN
# No especificar el indice para que pregunte
data = ReadLTSpice(folder="data", idx=None)
data.info() # Imprime información del archivo LTSpice (variables, casos, etc)

# plot_VL_C1 = [0, 4]
plot_VL_C1 = [1, 3]

print(len(data.varListInfo))

fig, ax1 = plt.subplots()
ax2 = None

def searchMaxMinInRange(x, y, t0, t1, ax = None, text = None, c='r'):
    # Search for the local maximum and minimum values in the range
    # Return two lists with the point coordinates

    max_points = []
    min_points = []

    for i in range(len(x))[1:]:
        if x[i] >= t0 and x[i] <= t1:
            if i == 0:
                if y[i] > y[i+1]:
                    max_points.append((x[i], y[i]))
                elif y[i] < y[i+1]:
                    min_points.append((x[i], y[i]))
            elif i == len(x) - 1:
                if y[i] > y[i-1]:
                    max_points.append((x[i], y[i]))
                elif y[i] < y[i-1]:
                    min_points.append((x[i], y[i]))
            else:
                if y[i] > y[i-1] and y[i] > y[i+1]:
                    max_points.append((x[i], y[i]))
                elif y[i] < y[i-1] and y[i] < y[i+1]:
                    min_points.append((x[i], y[i]))

    if ax is not None:
        # Plot the maxima and minima as red and blue dots, respectively
        for point in max_points:
            ax.scatter(point[0], point[1], c=c, marker='o')
            if text is not None:
                if text == "up":
                    ax.annotate(f'({point[0]:.2f}, {point[1]:.2f})', xy=(point[0], point[1]), xytext=(5, 5), textcoords='offset points')
                else:
                    ax.annotate(f'({point[0]:.2f}, {point[1]:.2f})', xy=(point[0], point[1]), xytext=(5, -15), textcoords='offset points')
        for point in min_points:
            ax.scatter(point[0], point[1], c=c, marker='o')
            if text is not None:
                if not text == "up":
                    ax.annotate(f'({point[0]:.2f}, {point[1]:.2f})', xy=(point[0], point[1]), xytext=(5, 5), textcoords='offset points')
                else:
                    ax.annotate(f'({point[0]:.2f}, {point[1]:.2f})', xy=(point[0], point[1]), xytext=(5, -15), textcoords='offset points')


    return max_points, min_points

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
                # _, h = searchMaxMinInRange(data.time, run, 0.005, 0.02, ax=ax2)
                # montecarloHist.append(h[0][1])

            else:
                ax1.plot(data.time, run, linewidth=1.0, color=color, alpha=0.4, label=showLabel)
                # _, h = searchMaxMinInRange(data.time, run, 0.01, 0.03, ax=ax1)
    
    # NOT MONTECARLO
    else:
        if data.varListInfo[i]["symbol"] == "I":
            ax2 = ax1.twinx()
            ax2.plot(data.time[0:40], data.varListData[i][0:40], linewidth=1.0, color=color, alpha=1.0, label=label)
            # searchMaxMinInRange(data.time, data.varListData[i], 0.0, 0.005, ax=ax2, text = "down")
        else:
            ax1.plot(data.time[0:40], data.varListData[i][0:40], linewidth=1.0, color=color, alpha=1.0, label=label)
            # searchMaxMinInRange(data.time, data.varListData[i], 0.005, 0.030, ax=ax1, text = "up")



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