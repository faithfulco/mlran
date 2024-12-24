# libraries
import os
import json
import pandas as pd
from tqdm import tqdm  # Import tqdm for the progress bar
import pickle
import time  # Import time to track duration

def extract_strings(report_path):
    """
    Extracts strings from a Cuckoo report without transforming them.
    Returns a dictionary with unique strings as keys and 1 as values (indicating the presence of the string).
    """
    strings_found = {}

    try:
        with open(report_path, 'r') as f:
            report = json.load(f)

        # Get the strings section from the report
        strings_section = report.get('strings', [])

        # Use a set to ensure unique strings
        unique_strings = set(strings_section)

        # Process each unique string in the strings section
        for string in unique_strings:
            string = string.lower()
            feature_name = f"STRING:{string}"
            strings_found[feature_name] = 1

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading {report_path}: {e}")

    return strings_found


def create_strings_dataframe(reports_folder):
    """
    Creates a DataFrame where each row is a report and each column is a unique string.
    The value is 1 if the string exists in that report, otherwise 0.
    """
    data = []
    all_features = set()

    # Get the list of all JSON files in the reports folder
    report_files = [f for f in os.listdir(reports_folder) if f.endswith(".json")]

    # Loop through all JSON files with progress bar
    for report_file in tqdm(report_files, desc="Processing reports", unit="file"):
        sample_id = report_file.split(".")[0]  # Extract sample ID (e.g., 10001 from 10001.json)
        report_path = os.path.join(reports_folder, report_file)

        # Extract strings for the current report
        strings_found = extract_strings(report_path)

        # Add the current sample ID and strings to the data list
        sample_data = {"sample_id": sample_id}
        sample_data.update(strings_found)
        data.append(sample_data)

        # Add the strings to the all_features set
        all_features.update(strings_found.keys())

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
    df5_str = create_strings_dataframe(reports_folder)
    display(df5_str)
