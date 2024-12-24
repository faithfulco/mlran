# libraries
import os
import json
import pandas as pd
from tqdm import tqdm  # Import tqdm for the progress bar
import pickle
import time  # Import time to track duration

def extract_network_operations(report_path):
    """
    Extracts network operations (connects_ip, connects_host, resolves_host)
    from a Cuckoo report.
    Returns a dictionary with keys as feature names and values as 1 (since the operation exists in this report).
    """
    network_operations = {}

    try:
        with open(report_path, 'r') as f:
            report = json.load(f)

        # Get the relevant network operations from behavior -> summary
        behavior_summary = report.get('behavior', {}).get('summary', {})

        # Process each network operation category
        for net_op in ['connects_ip', 'connects_host', 'resolves_host']:
            for network_item in behavior_summary.get(net_op, []):
                network_item = network_item.lower()
                feature_name = f"NETWORK:{net_op.upper()}:{network_item}"
                network_operations[feature_name] = 1

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading {report_path}: {e}")

    return network_operations


def create_network_operations_dataframe(reports_folder):
    """
    Creates a DataFrame where each row is a report and each column is a unique network operation.
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

        # Extract network operations for the current report
        network_operations = extract_network_operations(report_path)

        # Add the current sample ID and network operations to the data list
        sample_data = {"sample_id": sample_id}
        sample_data.update(network_operations)
        data.append(sample_data)

        # Add the network operations to the all_features set
        all_features.update(network_operations.keys())

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
    df6_net = create_network_operations_dataframe(reports_folder)
    display(df6_net)