# libraries
import os
import json
import pandas as pd
from tqdm import tqdm  # Import tqdm for the progress bar
import pickle
import time  # Import time to track duration

def extract_directory_operations(report_path):
    """
    Extracts directory operations (created and enumerated) from a Cuckoo report.
    Returns a dictionary with keys as feature names and values as 1 (since the operation exists in this report).
    """
    directory_operations = {}

    try:
        with open(report_path, 'r') as f:
            report = json.load(f)

        behavior_summary = report.get('behavior', {}).get('summary', {})

        # Mapping for directory operation names to the desired format
        directory_op_mapping = {
            'directory_created': 'CREATED',
            'directory_enumerated': 'ENUMERATED'
        }

        # Process directory operations
        for dir_op, formatted_name in directory_op_mapping.items():
            for dirpath in behavior_summary.get(dir_op, []):
                feature_name = f"DIRECTORY:{formatted_name}:{dirpath.lower()}"
                directory_operations[feature_name] = 1

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading {report_path}: {e}")

    return directory_operations

def create_directory_operations_dataframe(reports_folder):
    """
    Creates a DataFrame where each row is a report and each column is a unique directory operation.
    The value is 1 if the operation exists in that report, otherwise 0.
    """
    data = []
    all_features = set()

    # Get the list of all JSON files in the reports folder
    report_files = [f for f in os.listdir(reports_folder) if f.endswith(".json")]

    # Loop through all JSON files with progress bar
    for report_file in tqdm(report_files, desc="Processing reports", unit="file"):
        sample_id = report_file.split(".")[0]  # Extract sample ID (e.g., 10001 from 10001.json)
        report_path = os.path.join(reports_folder, report_file)

        directory_operations = extract_directory_operations(report_path)

        sample_data = {"sample_id": sample_id}
        sample_data.update(directory_operations)
        data.append(sample_data)

        all_features.update(directory_operations.keys())

    df = pd.DataFrame(data)

    df = df.reindex(columns=["sample_id"] + sorted(all_features), fill_value=0)
    df.fillna(0, inplace=True)
    df = df.astype(int)

    df['sample_id'] = df['sample_id'].astype(int)
    df.sort_values(by='sample_id', inplace=True)

    return df


# implementing the code
if __name__ == "__main__":
    reports_folder = "json_reports"  # Folder containing Cuckoo report JSON files
    df4_dir = create_directory_operations_dataframe(reports_folder)
    display(df4_dir)