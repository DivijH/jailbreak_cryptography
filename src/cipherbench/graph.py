import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Data for the bar graphs
categories = ["Short", "Short Random", "Long", "Long Random"]
values1 = [71, 18, 71, 6]
values2 = [40, 0, 35, 0]

# Create a DataFrame for the combined bar plot
data = pd.DataFrame({
    'Instance Categories': categories * 2,  # Repeat categories
    'Decryption Success Rate (DSR)': values1 + values2,  # Combine both sets of values
    'Model': ['GPT-4o'] * len(values1) + ['Gemini-1.5-Flash'] * len(values2)  # Model labels
})

# Set consistent colors for each plot
palette = {
    'GPT-4o': sns.color_palette("Blues_d")[2],  # Blue for GPT-4o
    'Gemini-1.5-Flash': sns.color_palette("Greens_d")[2]  # Green for Gemini-1.5-Flash
}

# Ensure non-zero values for 0 bars
data['Decryption Success Rate (DSR)'] = data['Decryption Success Rate (DSR)'].apply(lambda x: max(x, 1))

# Create a single bar plot with hue for the models
plt.figure(figsize=(8, 5))  # Reduced width by setting width to 6
sns.barplot(x='Instance Categories', y='Decryption Success Rate (DSR)', hue='Model', data=data, palette=palette)

# Remove the legend
plt.legend().remove()

# Set plot title with two lines and labels with increased font size
plt.title('Decryption Success Rate (DSR)\nby Instance Categories', fontsize=20, fontweight='bold')
plt.ylim(0, 100)  # Set y-axis limit from 0 to 100
plt.grid(True, which='major', axis='y', linestyle='--', alpha=0.7)

# Increase the size of the x-axis, y-axis labels
plt.gca().set_xlabel('', fontsize=18)
plt.gca().set_ylabel('', fontsize=18)
plt.xticks(fontsize=20, rotation=15)
plt.yticks(fontsize=20)

# Adjust layout and save the figure
plt.tight_layout()

# Save as PDF
plt.savefig('cipherbench.pdf')
