import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from adjustText import adjust_text
import numpy as np
from tabulate import tabulate

# Data for cosine based
# avg_data = {
#     'cosine based': [(128.9093, 0.4502256), (90.09188, 0.443774103), (86.28064, 0.465065799),
#                      (98.39355, 0.462286934)],
#     'power based': [(30.6316, 0.229573027), (29.83324, 0.208376794), (27.00062, 0.279494824), (26.01367, 0.26966333)],
#     'eosl based': [(44.6747, 0.368194861), (40.9862, 0.348891638), (35.16598, 0.40399214), (35.60491, 0.365201057)]
# }


# use this for BLEU based similarity plots

# Data for BLEU based
avg_data = {
    'BLEU based': [(79.5115, 0.1196647), (63.022, 0.110244418), (71.55888, 0.105193478), (75.00429, 0.098048677)],
    'power based': [(30.6316, 0.059927353), (29.83324, 0.045101937), (27.00062, 0.041305412), (26.01367, 0.049462235)],
    'eosl based': [(44.6747, 0.090038969), (29.83324, 0.075493305), (35.16598, 0.072268007), (35.60491, 0.0851841)]
}

# Labels for points
point_labels = {
    'BLEU based': ["Dogs", "Dogs+Surroundings", "Animals+interactions", "Animal Diversity"],
    'power based': ["Dogs", "Dogs+Surroundings", "Animals+interactions", "Animal Diversity"],
    'eosl based': ["Dogs", "Dogs+Surroundings", "Animals+interactions", "Animal Diversity"]
}

# Colors for each metric
colors = {
    'BLEU based': 'blue',
    'power based': 'green',
    'eosl based': 'red'
}

plt.figure(figsize=(10, 8))

# Plotting the points and circles
all_texts = []

for metric, values in avg_data.items():
    x = np.array([val[0] for val in values])  # X-axis
    y = np.array([val[1] for val in values])  # Y-axis
    labels = point_labels[metric]
    color = colors[metric]

    # Plot points
    plt.scatter(x, y, marker='o', color=color, label=metric)

    # Add text labels
    for (xi, yi, label) in zip(x, y, labels):
        txt = plt.text(xi, yi, label, fontsize=14, fontweight='bold', color=color)
        all_texts.append(txt)

    # Calculate the center of the circle (mean of points)
    center_x = np.mean(x)
    center_y = np.mean(y)

    # Calculate the width and height of the ellipse (4 standard deviations to ensure larger coverage)
    width = 4.5 * np.std(x)
    height = 4.5 * np.std(y)

    # Add dotted ellipse around the group of points
    ellipse = Ellipse((center_x, center_y), width, height, edgecolor=color, facecolor='none', linestyle='dotted')
    plt.gca().add_patch(ellipse)

# Adjust text to avoid overlap and add arrows
adjust_text(all_texts, arrowprops=dict(arrowstyle='->', color='black'))

plt.xlabel('Avg Power', fontsize=16)  # X-axis label with larger font size
plt.ylabel('Avg Similarity (BLEU based)', fontsize=16)  # Y-axis label with larger font size
plt.title('Comparison of Metrics', fontsize=16)  # Title with larger font size
plt.legend(loc='lower right', fontsize=16)  # Move legend to the bottom right and increase font size
plt.xticks(fontsize=16)  # Increase font size of x-axis ticks
plt.yticks(fontsize=16)  # Increase font size of y-axis ticks
plt.grid(True)
plt.show()


# # Use this for similarity to power ratio (SPR) table generation
# # (Change labels accordingly for cosine or BLEU based plots)
#
# # Function to calculate similarity/power ratio
# def calculate_ratio(data):
#     ratios = []
#     for point in data:
#         power, similarity = point
#         ratio = similarity / power
#         ratios.append(ratio)
#     return ratios
#
#
# # Create a table for the ratios
# table_data = []
# sample_sizes = [10, 25, 50, 100]
#
# for i, size in enumerate(sample_sizes):
#     row = [f"Sample Size {size}"]
#     for metric, points in avg_data.items():
#         ratio = calculate_ratio(points)[i]
#         row.append(f"{ratio * 1e3:.4f} x 10^-3")
#     table_data.append(row)
#
# # Print the table
# print(tabulate(table_data, headers=["Sample Size", "Similarity Based", "Power Based", "EOSL Based"]))
