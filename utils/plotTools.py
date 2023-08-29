import numpy as np
import matplotlib.pyplot as plt
from plotUtils import getGainPhase
from matplotlib.lines import Line2D

# top=0.961,
# bottom=0.163,
# left=0.085,
# right=0.902,
# hspace=0.2,
# wspace=0.2

def plotBode(h_data, frec, names=["", "Ideal"]):
    # check if h_data is a list
    if not isinstance(h_data, list):
        h_data = [h_data]

    # get gain and phase for each h_data
    gain = []
    phase = []
    for h in h_data:
        g, p = getGainPhase(h)
        gain.append(g)
        phase.append(p)

    # Create a figure and two axes
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    # Plot the gain and phase iterating with different line styles
    line_styles = ['-', '--', '-.', ':']
    for i, (g, p) in enumerate(zip(gain, phase)):
        ax1.semilogx(frec, g, lw=1.5, color='tab:red', linestyle=line_styles[i])
        ax2.semilogx(frec, p, lw=1.5, color='tab:blue', linestyle=line_styles[i])

    ax1.set_ylabel('Ganancia [dB]', color='tab:red')
    ax2.set_ylabel('Fase $[\degree]$', color='tab:blue')

    ax1.tick_params(axis='y', labelcolor='tab:red')
    ax1.grid(True, which="both", ls="-", axis="x")
    ax1.grid(True, which="both", ls="-", axis="y")

    ax2.tick_params(axis='y', labelcolor='tab:blue')
    ax2.grid(True, which="major", ls="-")

    ax1.xaxis.set_minor_locator(plt.LogLocator(base=10, subs='all', numticks=400))
    ax1.xaxis.set_major_locator(plt.LogLocator(base=10, numticks=100))

    # set ticks for ax2 y axis
    ax2.yaxis.set_major_locator(plt.MultipleLocator(15))
    ax1.yaxis.set_major_locator(plt.MultipleLocator(20))

    # Add a custom legend to the figure
    legend_lines = [Line2D([0], [0], color='tab:red', lw=2, linestyle=line_styles[i]) for i in range(len(h_data))]
    legend_lines += [Line2D([0], [0], color='tab:blue', lw=2, linestyle=line_styles[i]) for i in range(len(h_data))]
    legend_labels = ['Ganancia {}'.format(names[i]) for i in range(len(h_data))] + ['Fase {}'.format(names[i]) for i in range(len(h_data))]
    plt.legend(legend_lines, legend_labels, loc='upper right')

    ax1.set_xlabel('Frecuencia $[Hz]$')
    # plt.tight_layout()
    # plt.subplots_adjust(top=0.961, bottom=0.163, left=0.085, right=0.902, hspace=0.2, wspace=0.2)
    plt.show()