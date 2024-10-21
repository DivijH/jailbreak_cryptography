import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Data for the bar graphs
categories = ["Base 64", "ROT-13", "Pig Latin", "LeetSpeak", "Keyboard Cipher", "Upisde Down", "Word Reversal", "Word Substitution", "Grid Encoding", "ASCII Art Cipher"]
values1 = [30, 25, 19, 21, 2, 18, 25, 13, 12, 1] # GPT-4o
values2 = [19, 0, 10, 19, 0, 8, 6, 12, 1, 0] # Gemini-1.5-Flash

# Create a DataFrame for the combined bar plot
data = pd.DataFrame({
    'Ciphers': categories * 2,  # Repeat categories
    'Number of successful decryptions': values1 + values2,  # Combine both sets of values
    'Model': ['GPT-4o'] * len(values1) + ['Gemini-1.5-Flash'] * len(values2)  # Model labels
})

# Set consistent colors for each plot
palette = {
    'GPT-4o': sns.color_palette("Blues_d")[2],  # Blue for GPT-4o
    'Gemini-1.5-Flash': sns.color_palette("Greens_d")[2]  # Green for Gemini-1.5-Flash
}

# Ensure non-zero values for 0 bars
data['Number of successful decryptions'] = data['Number of successful decryptions'].apply(lambda x: max(x, 0.5))

# Create a single bar plot with hue for the models
plt.figure(figsize=(8, 5))  # Reduced width by setting width to 6
sns.barplot(x='Ciphers', y='Number of successful decryptions', hue='Model', data=data, palette=palette)

# Remove the legend
plt.legend().remove()

# Set plot title with two lines and labels with increased font size
plt.title('Number of successful decryptions\nby Ciphers', fontsize=20, fontweight='bold')
plt.ylim(0, 40)  # Set y-axis limit from 0 to 100
plt.grid(True, which='major', axis='y', linestyle='--', alpha=0.7)

# Increase the size of the x-axis, y-axis labels
plt.gca().set_xlabel('', fontsize=18)
plt.gca().set_ylabel('', fontsize=18)
plt.xticks(fontsize=20, rotation=30)
plt.yticks(fontsize=20)

# Adjust layout and save the figure
plt.tight_layout()

# Save as PDF
plt.savefig('cipherbench_ciphers.pdf')
