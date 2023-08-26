import numpy as np
import matplotlib.pyplot as plt
from utils.plotUtils import *


def OpAmpInv(s, KI, A0, wb):
    def KNI(s):
        return 1 - KI(s)

    def AvErr(s):
        return 1/(1 + KNI(s)/A0)

    def PoleErr(s):
        return 1/(1 + (s*KNI(s))/(wb*A0))
    
    return KI(s)*AvErr(s)*PoleErr(s)

def plotBode(e1, e2, H, points = 1000):
    w = np.logspace(e1, e2, points)

    # evaluate the complex function at each frequency
    s = 1j * w
    Hs = H(s)
    gain = 20 * np.log10(np.abs(Hs))
    phase = fixPhaseJumps(np.angle(Hs, deg=True))


    # Create a figure and two axes
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.semilogx(w, gain, color='tab:red', linestyle='-')
    ax1.set_ylabel('Magnitude')

    ax2.semilogx(w, phase, lw=2.5 , color='tab:blue', linestyle='--')
    ax2.set_xlabel('Frequency (rad/s)')
    ax2.set_ylabel('Phase (deg)')

    ax1.tick_params(axis='y', labelcolor='tab:red')
    ax1.grid(True, which="both", ls="-", axis="x")
    ax1.grid(True, which="both", ls="-", axis="y")

    ax2.tick_params(axis='y', labelcolor='tab:blue')
    ax2.grid(True, which="major", ls="--", color='black', alpha=1.0)

    ax1.xaxis.set_minor_locator(plt.LogLocator(base=10, subs='all', numticks=100))
    ax1.xaxis.set_major_locator(plt.LogLocator(base=10, numticks=30))

    plt.tight_layout()
    plt.show()