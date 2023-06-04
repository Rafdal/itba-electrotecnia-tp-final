import matplotlib.pyplot as plt
import numpy as np

# Create figure and axis objects
fig, ax = plt.subplots()

# Set x and y limits
r = 5
ax.set_xlim([-r, r])
ax.set_ylim([-r, r])

# Draw lines at x=0 and y=0
ax.axhline(y=0, color='black', linewidth=5.0, alpha=1.0)
ax.axvline(x=0, color='black', linewidth=5.0, alpha=1.0)

# Show the plot
plt.show()