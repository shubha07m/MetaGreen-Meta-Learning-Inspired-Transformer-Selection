import pandas as pd
import re

# Run below command for powermetrics collection: sudo powermetrics -i 1000  --samplers cpu_power,gpu_power -a
# --hide-cpu-duty-cycle --show-usage-summary --show-extra-power-info >> powersample_encoder.txt

# Read the data from the text file
data = pd.read_csv('powersample_encoder.txt', header=None)

Time_ = []
CPU_Power = []
GPU_Power = []
Combined_Power = []
j = 0
summary_index = -1

# Find the index of the line containing "Summary system activity"
for index, row in data.iterrows():
    if 'Summary system activity' in row[0]:
        summary_index = index
        break

# Process the data before the line with "Summary system activity"
for index, row in data.iloc[:summary_index].iterrows():
    if 'Sampled system activity' in row[0]:
        # Extract the timestamp from the line
        timestamp_match = re.search(r'\((.*?)\)', row[0])
        if timestamp_match:
            timestamp_str = timestamp_match.group(1)
            # Convert the timestamp to epoch format and append to Time_
            Time_.append(int(pd.Timestamp(timestamp_str).timestamp()))

    if 'CPU Power' in row[0]:
        if row[0][11:-3]:
            CPU_Power.append(float(row[0][11:-3]) / 1000)

    if 'GPU Power' in row[0]:
        j += 1
        if j % 2:
            if row[0][11:-3]:
                GPU_Power.append(float(row[0][11:-3]) / 1000)

    if 'Combined Power' in row[0]:
        if row[0][34:-3]:
            Combined_Power.append(float(row[0][34:-3]) / 1000)

# Create a DataFrame from the collected data
df = pd.DataFrame({'Time': Time_, 'CPU_Power': CPU_Power, 'GPU_Power': GPU_Power, 'Combined Power': Combined_Power})

# Save the DataFrame to a CSV file
df.to_csv('encoder_power_data.csv', index=False)
