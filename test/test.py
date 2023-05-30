import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# Define the transfer function H(s)
num = [1, 2]
den = [1, 3, 2]
H = signal.TransferFunction(num, den)

# Get the magnitude and phase of the transfer function
w, mag, phase = signal.bode(H)

print("w: ", w)

# plot w
x = np.linspace(0, 10, len(w))
plt.plot(x, w)
plt.show()

# Extract the numerator and denominator coefficients
num, den = H.num, H.den

# Create the Linear Time-Invariant system
lti_sys = signal.lti(num, den)

# Define the time vector and the input signal
t = np.linspace(0, 10, 1000)
x = np.sin(t)

# Apply the filter to the signal
tout, y, xout = signal.lsim(lti_sys, x, t)