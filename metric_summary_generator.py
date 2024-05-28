import pandas as pd
from eosl_helper_functions import eosl_loss, calculate_bleu_score
from tabulate import tabulate

# Global variables
beta = 0.3
operation = 'weighted_sum'

try:
    # Load historical EOSL data
    historical_eosl_df = pd.read_csv("historical_eosl.csv")
except FileNotFoundError:
    historical_eosl_df = pd.DataFrame()
    # If historical EOSL file not present, set operation to 'no_history'
    operation = 'no_history'

# Load the CSV files
timestamp_df = pd.read_csv("timestamps_encoder.csv")
resource_df = pd.read_csv("encoder_power_data.csv")
semantic_labels_df = pd.read_csv("semantic_labels.csv")


# Function to calculate total CPU_Power, GPU_Power, and Combined_Power used in a given interval
def calculate_total_power(start_time, end_time):
    filtered_rows = resource_df[(resource_df['Time'] >= start_time) & (resource_df['Time'] <= end_time)]
    total_cpu_power = filtered_rows['CPU_Power'].sum()
    total_gpu_power = filtered_rows['GPU_Power'].sum()
    total_combined_power = filtered_rows['Combined Power'].sum()
    return total_cpu_power, total_gpu_power, total_combined_power


# Function to calculate EOSL and similarity, considering historical data
def add_eosl_similarity_column(df):
    def calculate_eosl_for_row(row):
        img = row['Image']
        model = row['Model Name']
        Mi = row['Defined Semantics']
        Mp = row['Generated Caption']

        # Initialize eosl and similarity
        eosl, similarity = 0, 0

        if operation == 'no_history':
            eosl, similarity = eosl_loss(df, img, model, Mi, Mp)
        else:
            historical_eosl_row = historical_eosl_df[
                (historical_eosl_df['Image'] == img) & (historical_eosl_df['Model Name'] == model)]
            if not historical_eosl_row.empty:
                historical_eosl = historical_eosl_row.iloc[0]['Encoder EOSL']
                eosl, similarity = eosl_loss(df, img, model, Mi, Mp)
                if operation == 'weighted_sum':
                    updated_eosl = historical_eosl * beta + (1 - beta) * eosl
                    eosl = updated_eosl
                elif operation == 'multiplication':
                    eosl *= historical_eosl
                elif operation == 'addition':
                    eosl += historical_eosl
            else:
                eosl, similarity = eosl_loss(df, img, model, Mi, Mp)

        return eosl, similarity

    df[['Encoder EOSL', 'Cosine Similarity']] = df.apply(calculate_eosl_for_row, axis=1, result_type='expand')
    return df


# Calculate total power and add EOSL and similarity columns
data = {'Image': [], 'Model Name': [], 'Defined Semantics': [], 'Generated Caption': [],
        'Total CPU Power': [], 'Total GPU Power': [], 'Total Combined Power': [],
        'BLEU Score': []}  # Add 'BLEU Score' column
for _, row in timestamp_df.iterrows():
    image = row['Image'].split('/')[-1]
    generated_caption = row['GeneratedCaption']
    model_name = row['ModelName']
    start_time = row['StartTime']
    end_time = row['EndTime']
    total_cpu_power, total_gpu_power, total_combined_power = calculate_total_power(start_time, end_time)
    defined_semantic = semantic_labels_df[semantic_labels_df['Image'] == image]['Defined Semantics'].iloc[0]

    bleu_score = calculate_bleu_score(generated_caption, defined_semantic)

    data['Image'].append(image)
    data['Model Name'].append(model_name)
    data['Defined Semantics'].append(defined_semantic)
    data['Generated Caption'].append(generated_caption)
    data['Total CPU Power'].append(total_cpu_power)
    data['Total GPU Power'].append(total_gpu_power)
    data['Total Combined Power'].append(total_combined_power)
    data['BLEU Score'].append(bleu_score)  # Append BLEU score

# Create a DataFrame from the collected data
final_df = pd.DataFrame(data)

# Calculate EOSL and similarity using the modified function with the specified operation
final_df = add_eosl_similarity_column(final_df.copy())

# Save the DataFrame as a new CSV file based on the operation used
final_df.sort_values(by='Image').to_csv('encoder_summary_' + operation + '.csv', index=False)

# Winner based on Total Combined Power
encode_power_winner_df = final_df.loc[final_df.groupby('Image')['Total Combined Power'].idxmin()]
encode_power_avg_combined_power = encode_power_winner_df['Total Combined Power'].mean()
encode_power_avg_similarity = encode_power_winner_df['Cosine Similarity'].mean()

# Winner based on EOSL
eosl_winner_df = final_df.loc[final_df.groupby('Image')['Encoder EOSL'].idxmin()]
eosl_avg_combined_power = eosl_winner_df['Total Combined Power'].mean()
eosl_avg_similarity = eosl_winner_df['Cosine Similarity'].mean()

# Winner based on Similarity
similarity_winner_df = final_df.loc[final_df.groupby('Image')['Cosine Similarity'].idxmax()]
similarity_avg_combined_power = similarity_winner_df['Total Combined Power'].mean()
similarity_avg_similarity = similarity_winner_df['Cosine Similarity'].mean()

# Save the winner tables as CSV files
encode_power_winner_df[['Image', 'Model Name', 'Total Combined Power', 'Cosine Similarity', 'BLEU Score']].to_csv(
    'encode_power_winner_summary.csv', index=False)
eosl_winner_df[['Image', 'Model Name', 'Total Combined Power', 'Cosine Similarity', 'BLEU Score']].to_csv(
    'eosl_winner_summary.csv', index=False)
similarity_winner_df[['Image', 'Model Name', 'Total Combined Power', 'Cosine Similarity', 'BLEU Score']].to_csv(
    'cosine_similarity_winner_summary.csv', index=False)

# Winner based on BLEU Score
bleu_winner_df = final_df.loc[final_df.groupby('Image')['BLEU Score'].idxmax()]
bleu_avg_combined_power = bleu_winner_df['Total Combined Power'].mean()
bleu_avg_similarity = bleu_winner_df['Cosine Similarity'].mean()

# Save the winner table based on BLEU score as a CSV file
bleu_winner_df[['Image', 'Model Name', 'Total Combined Power', 'Cosine Similarity', 'BLEU Score']].to_csv(
    'bleu_similarity_winner_summary.csv', index=False)