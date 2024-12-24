# libraries
import os
import json
import pandas as pd
from tqdm import tqdm  # Import tqdm for the progress bar
import pickle
import time  # Import time to track duration

def extract_signature_operations(report_path):
    """
    Extracts signature names from the Cuckoo report.
    Returns a dictionary with keys as signature names and values as 1 (since the signature is present).
    """
    with open(report_path, 'r') as f:
        report = json.load(f)

    signature_operations = {}

    # Get the relevant signatures from the report
    signatures = report.get('signatures', [])

    # Process each signature
    for signature in signatures:
        signature_name = f"SIGNATURE:{signature['name'].lower()}"
        signature_operations[signature_name] = 1  # Set to 1 since the signature is present

    return signature_operations


def create_signature_operations_dataframe(reports_folder):
    """
    Creates a DataFrame where each row is a report and each column is a unique signature name.
    The value is 1 if the signature is present in that report, otherwise 0.
    """
    # List to store data for each sample
    data = []

    # Set to collect all unique feature names (signature names)
    all_features = set()

    # Get the list of all JSON files in the reports folder
    report_files = [f for f in os.listdir(reports_folder) if f.endswith(".json")]

    # Loop through all JSON files with progress bar
    for report_file in tqdm(report_files, desc="Processing reports", unit="file"):
        sample_id = report_file.split(".")[0]  # Extract sample ID (e.g., 10001 from 10001.json)
        report_path = os.path.join(reports_folder, report_file)

        # Extract signature operations for the current report
        signature_operations = extract_signature_operations(report_path)

        # Add the current sample ID and signature operations to the data list
        sample_data = {"sample_id": sample_id}
        sample_data.update(signature_operations)
        data.append(sample_data)

        # Add the signature names to the all_features set
        all_features.update(signature_operations.keys())

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

    return df


# implementing the code
if __name__ == "__main__":
    reports_folder = "json_reports"  # Folder containing Cuckoo report JSON files
    df9_sig = create_signature_operations_dataframe(reports_folder)
    display(df9_sig)
