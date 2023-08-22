import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from utils.plotTools import *

# define the complex function
def H(s):
    return 1 / (s + 30j)


# plot the bode plot
plotBode(-2, 2, H)