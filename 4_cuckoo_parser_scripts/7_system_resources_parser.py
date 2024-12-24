# libraries
import os
import json
import pandas as pd
from tqdm import tqdm  # Import tqdm for the progress bar
import pickle
import time  # Import time to track duration

def extract_system_operations(report_path):
    """
    Extracts system operations (dll_loaded, command_line, mutex, guid) from a Cuckoo report.
    Returns a dictionary with keys as feature names and values as 1 (since the operation exists in this report).
    """
    system_operations = {}

    try:
        with open(report_path, 'r') as f:
            report = json.load(f)

        # Get the relevant system operations from behavior -> summary
        behavior_summary = report.get('behavior', {}).get('summary', {})

        # Process each system operation category
        for sys_op in ['dll_loaded', 'command_line', 'mutex', 'guid']:
            for system_item in behavior_summary.get(sys_op, []):
                system_item = system_item.lower()
                # Generate the feature name directly
                feature_name = f"SYSTEM:{sys_op.upper()}:{system_item}"
                system_operations[feature_name] = 1

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading {report_path}: {e}")

    return system_operations


def create_system_operations_dataframe(reports_folder):
    """
    Creates a DataFrame where each row is a report and each column is a unique system operation.
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

        # Extract system operations for the current report
        system_operations = extract_system_operations(report_path)

        # Add the current sample ID and system operations to the data list
        sample_data = {"sample_id": sample_id}
        sample_data.update(system_operations)
        data.append(sample_data)

        # Add the system operations to the all_features set
        all_features.update(system_operations.keys())

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
    df7_sys = create_system_operations_dataframe(reports_folder)
    display(df7_sys)
