import matplotlib.pyplot as plt

# alimentado a 4.5V
a_74HC00 = {
    # INPUT
    "VIH": 2.4,
    "VIL": 2.1,
    # OUTPUT
    "VOH": 4.5,
    "VOL": 0.0,
}

# alimentado a 4.5V
a_74HS02 = {
    # INPUT
    "VIH": 2,
    "VIL": 0.8,
    # OUTPUT
    "VOH": 3.4,
    "VOL": 0.35,
}

stripe_width = 0.5

# Create the figure and axis
fig, ax = plt.subplots()

def drawStripe(y_max, y_min, x_start, x_end, text="text", color='blue'):
    # Plot the stripe
    ax.axhspan(y_min, y_max, xmin=x_start, xmax=x_end, facecolor=color, alpha=0.5)

    # add text label
    ax.text((x_end + x_start)/2.5, (y_max+y_min)/2, f'{text}', ha='left', va='center', fontsize=10)
    # Plot the polygon
    # Define the polygon's vertices
    x_st = x_end
    x = [x_st, x_st + 0.03, x_st]
    y = [y_max, (y_max+y_min)/2, y_min]
    ax.fill(x, y, facecolor='blue', alpha=0.5)


drawStripe(a_74HC00["VIH"], a_74HC00["VIL"], 0, stripe_width, "VIH", 'blue')

# Set the axis limits and labels
ax.set_xlim([0, 1])
ax.set_ylim([0, 4])
ax.set_xlabel('X')
ax.set_ylabel('Tensión $[V]$')

# Show the plot
plt.show()