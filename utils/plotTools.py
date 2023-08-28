import numpy as np
import matplotlib.pyplot as plt
from plotUtils import getGainPhase

def plotBode(h_data, frec):
    gain, phase = getGainPhase(h_data)

    # Create a figure and two axes
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.semilogx(frec, gain, color='tab:red', linestyle='-')
    ax1.set_ylabel('Ganancia [dB]')

    ax2.semilogx(frec, phase, lw=2.5 , color='tab:blue', linestyle='-')
    ax2.set_xlabel('Frecuencia $[Hz]$')
    ax2.set_ylabel('Fase $[\degree]$')

    ax1.tick_params(axis='y', labelcolor='tab:red')
    ax1.grid(True, which="both", ls="-", axis="x")
    ax1.grid(True, which="both", ls="-", axis="y")

    ax2.tick_params(axis='y', labelcolor='tab:blue')
    ax2.grid(True, which="major", ls="--")

    ax1.xaxis.set_minor_locator(plt.LogLocator(base=10, subs='all', numticks=100))
    ax1.xaxis.set_major_locator(plt.LogLocator(base=10, numticks=30))

    # set ticks for ax2 y axis
    ax2.yaxis.set_major_locator(plt.MultipleLocator(10))

    plt.tight_layout()
    plt.show()