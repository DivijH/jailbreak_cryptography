import matplotlib.pyplot as plt
import numpy as np

# Data
ENCODINGS = ['Keyboard Cipher', 'UpsideDown', 'Word Reversal Cipher', 'Grid Encoding', 'Word Substitution']
GPT_4o = [3, 4, 6, 3, 6]
Gemini = [2, 5, 4, 1, 8]
categories = ENCODINGS

# Number of variables
N = len(categories)

# What will be the angle of each axis in the plot (we divide the plot / number of variables)
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
angles += angles[:1]  # to complete the loop

# Initialize the spider plot
fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))

# Set theta offset and direction
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

# Dark grey background and white grid
ax.set_facecolor('#D3D3D3')  # Dark grey background
ax.spines['polar'].set_color('white')
ax.tick_params(colors='black')  # White ticks
ax.grid(color='white', linestyle='--')

# Draw one axis per variable and add labels with increased font size and white color
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=15, color='black')  # Increased font size and white color

# Data for GPT
GPT_values = GPT_4o + GPT_4o[:1]  # complete the loop
ax.plot(angles, GPT_values, linewidth=2, linestyle='solid', label='GPT', color='#4949b1')
ax.fill(angles, GPT_values, '#4949b1', alpha=0.25)
ax.scatter(angles[:-1], GPT_4o, color='#4949b1', s=100, zorder=3)  # Add dots for GPT data

# Data for Gemini
Gemini_values = Gemini + Gemini[:1]  # complete the loop
ax.plot(angles, Gemini_values, linewidth=2, linestyle='solid', label='Gemini', color='#ff7e00')
ax.fill(angles, Gemini_values, '#ff7e00', alpha=0.25)
ax.scatter(angles[:-1], Gemini, color='#ff7e00', s=100, zorder=3)  # Add dots for Gemini data

# Set y-ticks (scaling)
ax.set_yticks(range(1, 11, 2))  # Scale out of 10
ax.set_yticklabels(range(1, 11, 2), color='black', fontsize=15)  # White y-tick labels with larger font size

# Increase the font size of the legend
ax.legend(loc='upper right', fontsize=15, facecolor='white', framealpha=1, edgecolor='black')

# Save the figure as a PDF
plt.tight_layout()
fig.savefig('overdefense.pdf')

plt.show()
