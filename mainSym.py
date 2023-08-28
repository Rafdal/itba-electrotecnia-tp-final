import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from utils.plotTools import *

# define the complex function
R = 5100
r = 5100
C = 10*10**(-9)
A0 = 223000
wb = 15 * 2 * np.pi

def ki_der(s):
    return (-s*R*C)/(1+s*r*C)

def H(s):
    return OpAmpInv(s, ki_der, A0, wb)

# plot the bode plot
plotBode(-2, 8, H)

def pole_err(s):
    return 1/(1 + s/())


