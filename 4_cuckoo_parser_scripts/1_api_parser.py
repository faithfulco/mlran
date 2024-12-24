# libraries
import os
import json
import pandas as pd
from tqdm import tqdm  # Import tqdm for the progress bar
import pickle
import time  # Import time to track duration

def summarize_api_calls(apistats):
    """
    Summarizes API calls from the apistats section of the report.
    Returns a dictionary with keys as feature names prefixed with "API:" and values as 1 (since the API was called).
    """
    # Find all unique API calls across all processes
    unique_api_calls = set()
    for api_dict in apistats.values():
        unique_api_calls.update(api_dict.keys())

    # Initialize a dictionary to store the summary with "API:" prefix
    summary = {f"API:{api}": 0 for api in unique_api_calls}

    # Set called API calls to 1
    for api_dict in apistats.values():
        for api in api_dict.keys():
            summary[f"API:{api}"] = 1

    return summary

def process_reports_folder(reports_folder):
    """
    Processes all JSON report files in the specified folder and returns a DataFrame
    with summarized API calls for each report.
    """
    # Initialize a list to store rows of data
    data = []
    file_ids = []

    # Loop through all JSON files in the reports folder with progress bar
    all_files = [f for f in os.listdir(reports_folder) if f.isdigit() or f.endswith('.json')]

    # Initialize tqdm progress bar
    for filename in tqdm(all_files, desc="Processing files", unit="file"):
        file_path = os.path.join(reports_folder, filename)
        with open(file_path, 'r') as file:
            report = json.load(file)
            apistats = report.get('behavior', {}).get('apistats', {})
            summary = summarize_api_calls(apistats)
            file_id = os.path.splitext(filename)[0]  # Extract file ID (e.g., 10001)
            data.append(summary)
            file_ids.append(int(file_id))  # Convert file ID to integer for sorting

    # Create a DataFrame from the list of summaries and set the index as "sample_id"
    df = pd.DataFrame(data, index=file_ids).fillna(0).astype(int).rename_axis("sample_id")

    # Sort the DataFrame by sample_id to ensure it's in order (10001, 10002, etc.)
    df.sort_index(inplace=True)

    return df

if __name__ == "__main__":
    reports_folder = "json_reports" # Folder containing Cuckoo report JSON files
    df1_api = process_reports_folder(reports_folder)
    display(df1_api)
