# libraries
import os
import json
import pandas as pd
from tqdm import tqdm  # Import tqdm for the progress bar
import pickle
import time  # Import time to track duration

def extract_dropped_file_features(report_path):
    """
    Extracts dropped file extensions and types from the dropped section of a Cuckoo report.
    Returns a dictionary with keys as feature names and values as 1.
    The feature names start with 'DROP'.
    """
    dropped_features = {}

    try:
        with open(report_path, 'r') as f:
            report = json.load(f)

        # Get the dropped files section
        dropped_files = report.get('dropped', [])

        # Initialize sets for unique file extensions and types
        file_extension_set = set()
        file_type_set = set()

        # Process each dropped file
        for file_info in dropped_files:
            file_name = file_info.get('name', '')
            file_type = file_info.get('type', '')

            # Extract file extension
            if '.' in file_name:
                file_extension = file_name.split('.')[-1].lower()
                file_extension_set.add(file_extension)

            # Extract file type
            if file_type:
                file_type_set.add(file_type)

        # Create features for unique file extensions and types
        for ext in file_extension_set:
            dropped_features[f"DROP:EXTENSION:{ext.lower()}"] = 1
        for ftype in file_type_set:
            dropped_features[f"DROP:TYPE:{ftype.replace(' ', '_').lower()}"] = 1

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading {report_path}: {e}")

    return dropped_features


def create_dropped_file_features_dataframe(reports_folder):
    """
    Creates a DataFrame where each row is a report and each column is a unique dropped file extension.
    The value is 1 if the extension exists in that report, otherwise 0.
    """
    data = []
    all_features = set()

    # Get the list of all JSON files in the reports folder
    report_files = [f for f in os.listdir(reports_folder) if f.endswith(".json")]

    # Loop through all JSON files with progress bar
    for report_file in tqdm(report_files, desc="Processing reports", unit="file"):
        sample_id = report_file.split(".")[0]  # Extract sample ID (e.g., 10001 from 10001.json)
        report_path = os.path.join(reports_folder, report_file)

        # Extract dropped file extensions for the current report
        dropped_extensions = extract_dropped_file_features(report_path)

        # Add the current sample ID and dropped file extensions to the data list
        sample_data = {"sample_id": sample_id}
        sample_data.update(dropped_extensions)
        data.append(sample_data)

        # Add the dropped file extensions to the all_features set
        all_features.update(dropped_extensions.keys())

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
    df8_drop = create_dropped_file_features_dataframe(reports_folder)
    display(df8_drop)