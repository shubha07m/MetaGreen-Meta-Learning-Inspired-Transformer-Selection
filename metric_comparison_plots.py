import matplotlib.pyplot as plt
from tabulate import tabulate
from adjustText import adjust_text
# use this for cosine based similarity plots
# addition with a decay_rate = 0.3

avg_data = {
    'cosine based': [(128.9093, 0.4502256), (90.09188, 0.443774103), (86.28064, 0.465065799),
                         (98.39355, 0.462286934)],
    'power based': [(30.6316, 0.229573027), (29.83324, 0.208376794), (27.00062, 0.279494824), (26.01367, 0.26966333)],
    'eosl based': [(44.6747, 0.368194861), (40.9862, 0.348891638), (35.16598, 0.40399214), (35.60491, 0.365201057)]
}


# use this for BLEU based similarity plots

# avg_data = {
#     'BLEU based': [(79.5115, 0.1196647), (63.022, 0.110244418), (71.55888,0.105193478), (75.00429, 0.098048677)],
#     'power based': [(30.6316, 0.059927353), (29.83324, 0.045101937), (27.00062, 0.041305412), (26.01367, 0.049462235)],
#     'eosl based': [(44.6747, 0.090038969), (29.83324, 0.075493305), (35.16598, 0.072268007), (35.60491, 0.0851841)]
# }


# use this for generating plots #

# Text to be displayed near each point (bold)
# (Change labels accordingly for cosine or BLEU based plots)
point_labels = {
    'cosine based': ["Dogs", "Dogs+Surroundings", "Animals+interactions", "Animal Diversity"],
    'power based': ["Dogs", "Dogs+Surroundings", "Animals+interactions", "Animal Diversity"],
    'eosl based': ["Dogs", "Dogs+Surroundings", "Animals+interactions", "Animal Diversity"]
}
#
# Colors for each metric
colors = {
    'cosine based': 'blue',
    'power based': 'green',
    'eosl based': 'red'
}

# Plot
plt.figure(figsize=(8, 6))

# Plot each metric type
for metric, values in avg_data.items():
    x = [val[0] for val in values]  # X-axis
    y = [val[1] for val in values]  # Y-axis
    labels = point_labels[metric]
    color = colors[metric]
    plt.scatter(x, y, marker='o', color=color, label=metric)
    for i, (x_val, y_val) in enumerate(zip(x, y)):
        plt.text(x_val, y_val, labels[i], fontsize=10, fontweight='bold', ha='left', va='bottom')

plt.xlabel('Avg Power')  # X-axis label
plt.ylabel('Avg Similarity (cosine based)')  # Y-axis label
plt.title('Comparison of Metrics')
plt.legend(loc='upper left')  # Move legend to the left
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
