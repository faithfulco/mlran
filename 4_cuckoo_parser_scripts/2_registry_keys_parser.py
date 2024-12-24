# libraries
import os
import json
import pandas as pd
from tqdm import tqdm  # Import tqdm for the progress bar
import pickle
import time  # Import time to track duration

def extract_registry_operations(report_path):
    """
    Extracts registry key operations (opened, deleted, read, written) from a Cuckoo report.
    Returns a dictionary with keys as feature names and values as 1 (since the key exists in this report).
    """
    with open(report_path, 'r') as f:
        report = json.load(f)

    registry_features = {}

    # Get the relevant registry operations from behavior -> summary
    behavior_summary = report.get('behavior', {}).get('summary', {})

    # Process regkey_opened
    for regkey in behavior_summary.get('regkey_opened', []):
        feature_name = f"REG:OPENED:{regkey}"
        registry_features[feature_name] = 1

    # Process regkey_deleted
    for regkey in behavior_summary.get('regkey_deleted', []):
        feature_name = f"REG:DELETED:{regkey}"
        registry_features[feature_name] = 1

    # Process regkey_read
    for regkey in behavior_summary.get('regkey_read', []):
        feature_name = f"REG:READ:{regkey}"
        registry_features[feature_name] = 1

    # Process regkey_written
    for regkey in behavior_summary.get('regkey_written', []):
        feature_name = f"REG:WRITTEN:{regkey}"
        registry_features[feature_name] = 1

    return registry_features


def create_registry_dataframe(reports_folder):
    """
    Creates a DataFrame where each row is a report and each column is a unique registry key operation.
    The value is 1 if the operation exists in that report, otherwise 0.
    """
    # Start timing the process
    start_time = time.time()

    # List to store data for each sample
    data = []

    # Set to collect all unique feature names (registry key operations)
    all_features = set()

    # Get the list of all JSON files in the reports folder
    report_files = [f for f in os.listdir(reports_folder) if f.endswith(".json")]

    # Loop through all JSON files with progress bar
    for report_file in tqdm(report_files, desc="Processing reports", unit="file"):
        sample_id = report_file.split(".")[0]  # Extract sample ID (e.g., 10001 from 10001.json)
        report_path = os.path.join(reports_folder, report_file)

        # Extract registry operations for the current report
        registry_features = extract_registry_operations(report_path)

        # Add the current sample ID and registry features to the data list
        sample_data = {"sample_id": sample_id}
        sample_data.update(registry_features)
        data.append(sample_data)

        # Add the registry features to the all_features set
        all_features.update(registry_features.keys())

    # Create a DataFrame from the collected data
    df = pd.DataFrame(data)

    # Ensure all features (columns) are in the DataFrame, fill missing values with 0
    df = df.reindex(columns=["sample_id"] + sorted(all_features), fill_value=0)

    # Replace NaN with 0 and convert the DataFrame to integers
    df.fillna(0, inplace=True)
    df = df.astype(int)  # Ensure all values are integers (1 or 0)

    # Sort rows by sample_id in ascending order
    df['sample_id'] = df['sample_id'].astype(int)  # Convert sample_id to int for sorting
    df.sort_values(by='sample_id', inplace=True)

    # End timing the process
    end_time = time.time()

    # Calculate the total time taken and print it
    total_time = end_time - start_time
    print(f"\nTotal time to process and create the registry dataframe: {total_time:.2f} seconds")

    return df

# Implementing the code
reports_folder = "json_reports" # Folder containing Cuckoo report JSON files
df2_reg = create_registry_dataframe(reports_folder)
display(df2_reg)