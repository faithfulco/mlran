# libraries
import os
import json
import pandas as pd
from tqdm import tqdm  # Import tqdm for the progress bar
import pickle
import time  # Import time to track duration

def extract_file_operations(report_path):
    """
    Extracts file operations (created, recreated, opened, written, deleted, exists, failed, read) from a Cuckoo report.
    Returns a dictionary with keys as feature names and values as 1 (since the operation exists in this report).
    """
    file_operations = {}

    try:
        with open(report_path, 'r') as f:
            report = json.load(f)

        behavior_summary = report.get('behavior', {}).get('summary', {})

        # Mapping for file operation names to the desired format
        file_op_mapping = {
            'file_created': 'CREATED',
            'file_recreated': 'RECREATED',
            'file_opened': 'OPENED',
            'file_written': 'WRITTEN',
            'file_deleted': 'DELETED',
            'file_exists': 'EXISTS',
            'file_failed': 'FAILED',
            'file_read': 'READ'
        }

        for file_op, formatted_name in file_op_mapping.items():
            for filepath in behavior_summary.get(file_op, []):
                # Construct feature name with FILE and FORMATTED NAME in uppercase
                # Convert filepath to lowercase to ensure uniqueness
                feature_name = f"FILE:{formatted_name}:{filepath.lower()}"
                file_operations[feature_name] = 1

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading {report_path}: {e}")

    return file_operations

def create_file_operations_dataframe(reports_folder):
    """
    Creates a DataFrame where each row is a report and each column is a unique file operation.
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

        file_operations = extract_file_operations(report_path)

        sample_data = {"sample_id": sample_id}
        sample_data.update(file_operations)
        data.append(sample_data)

        all_features.update(file_operations.keys())

    df = pd.DataFrame(data)

    # Ensure columns are sorted and all feature names are unique (case-insensitive)
    df = df.reindex(columns=["sample_id"] + sorted(all_features), fill_value=0)
    df.fillna(0, inplace=True)
    df = df.astype(int)

    df['sample_id'] = df['sample_id'].astype(int)
    df.sort_values(by='sample_id', inplace=True)

    return df

# implementing the code
if __name__ == "__main__":
    reports_folder = "json_reports"  # Folder containing Cuckoo report JSON files
    df3_file = create_file_operations_dataframe(reports_folder)
    display(df3_file)
