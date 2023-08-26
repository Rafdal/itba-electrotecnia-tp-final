import sympy as sp
import numpy as np
from plotUtils import getGainPhase
from plotTools import plotBode
import matplotlib.pyplot as plt

# Define the sp.symbols used in the equation
s = sp.symbols('s', real=False)
R, C, r = sp.symbols('R C r', positive=True, real=True)
a0, wb = sp.symbols('a0 wb', positive=True, real=True)

# Define the equation to be simplified
# ki = -s*R*C     # derivador sin compensar
ki = (-s*R*C)/(s*r*C + 1)     # derivador compensado
# ki = 

kni = 1 - ki

arr_a0 = 1/(1 + kni/a0)
err_polo = 1/(1 + (s*kni)/(wb*a0))
err_polo1 = 1/(1 + s/(wb*(-a0/ki + 1)))

h = ki * arr_a0 * err_polo
h1 = ki * arr_a0 * err_polo1

# Simplify the equation
simplified_h = sp.simplify(h)
simplified_h1 = sp.simplify(h1)

# Print the original and simplified equations
print("ki:", ki)
print("kni:", kni)
print("arr_a0:", arr_a0)
print("err_polo:", err_polo)
print('Original equation:', h)
print('Simplified equation:', simplified_h)
print('Simplified equation1:', simplified_h1)

# Define the sp.symbols values used in the equation
R_val = 5100
r_val = 0
C_val = 10*1e-9
a0_val = 223000
wb_val = 2*sp.pi*15

# Substitute the values in the simplified equation
simplified_h = simplified_h.subs(R, R_val).subs(C, C_val).subs(a0, a0_val).subs(wb, wb_val).subs(r, r_val)
simplified_h1 = simplified_h1.subs(R, R_val).subs(C, C_val).subs(a0, a0_val).subs(wb, wb_val).subs(r, r_val)

# Define a function to evaluate the equation with the values
h_func = sp.lambdify(s, simplified_h, 'numpy')
h_func1 = sp.lambdify(s, simplified_h1, 'numpy')

# Define a logspace vector for the frequency used with the s complex variable
frec = np.logspace(0, 10, 5000)
s_val = 1j*2*np.pi*frec

h_val = np.array(h_func(s_val))
h_val1 = np.array(h_func1(s_val))
print("h_val shape:", h_val.shape)
# h_val = h_val.reshape(1, len(h_val))


# Plot the gain and phase
gain, phase = getGainPhase(h_val)
gain1, phase1 = getGainPhase(h_val1)

# Create a figure and two axes
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.semilogx(frec, gain, color='tab:red', label='No ideal', linestyle='-')
ax1.semilogx(frec, gain1, color='tab:red', label='No ideal1', linestyle='--')
ax1.tick_params(axis='y', labelcolor='tab:red')
ax1.grid(True, which="both", ls="-", axis="x")
ax1.grid(True, which="both", ls="-", axis="y")
# ax1.yaxis.set_minor_locator(plt.LogLocator(base=10, subs='all', numticks=200))
# ax1.yaxis.set_major_locator(plt.LogLocator(base=10, numticks=50))
# SET TICKS

ax2.semilogx(frec, phase, color='tab:blue', linestyle='-', label='No ideal')
ax2.semilogx(frec, phase1, color='tab:blue', linestyle='--', label='No ideal1')
ax2.tick_params(axis='y', labelcolor='tab:blue')
ax2.grid(True, which="major", ls="--", color='black', alpha=1.0)


# Set axis locators
ax1.xaxis.set_minor_locator(plt.LogLocator(base=10, subs='all', numticks=200))
ax1.xaxis.set_major_locator(plt.LogLocator(base=10, numticks=50))

# Set the labels
ax1.set_xlabel('Frecuencia $[Hz]$')
ax1.set_ylabel('Ganancia [dB]', color='tab:red')
# ax1.set_ylabel('Zin Magnitude [$\Omega$]', color='tab:red')
ax2.set_ylabel('Fase $[\degree]$', color='tab:blue')

# Adjust the layout of the plot
fig.tight_layout()

# Show the plot
plt.show()


# Set up LaTeX rendering
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"]
})

# Render LaTeX expression as image
fig1, ax = plt.subplots()
text = sp.latex(simplified_h)
ax.text(0.5, 0.5, text, fontsize=24, ha="center", va="center")
ax.axis("off")
plt.show()