# Import libraries
import os
import hashlib
import pandas as pd

def calculate_hashes(file_path):
    """
    Calculate SHA-256, SHA-1, and MD5 hashes for the given file.

    Args:
        file_path (str): The path to the file.

    Returns:
        dict: A dictionary containing the hexadecimal digests of the hashes.
    """
    # Initialize hash objects
    hashes = {
        'sha256': hashlib.sha256(),
        'sha1': hashlib.sha1(),
        'md5': hashlib.md5()
    }

    # Read file in binary mode and update hash objects
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            for h in hashes.values():
                h.update(chunk)

    # Return the hexadecimal digest of each hash
    return {name: h.hexdigest() for name, h in hashes.items()}

def get_file_hashes(directory):
    """
    Get hashes of all visible files in the specified directory, excluding subdirectories and unwanted files.

    Args:
        directory (str): The path to the directory.

    Returns:
        pd.DataFrame: A DataFrame containing filenames and their hashes.
    """
    files_data = []

    # List files in the specified directory, excluding hidden and unwanted files
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path) and not file.startswith('.') and not file.startswith('~$') and file != 'desktop.ini':
            # Calculate hashes for the file
            hashes = calculate_hashes(file_path)
            files_data.append({
                'filename': file,
                **hashes
            })

    # Create and return a DataFrame with the file hashes
    return pd.DataFrame(files_data)


# Specify the directory containing the files
directory = 'insert/the/path/to/your/folder'
file_hashes_df = get_file_hashes(directory)

# Display the DataFrame
display(file_hashes_df)

# Save the DataFrame to a CSV file if needed
file_hashes_df.to_csv('file_hashes.csv', index=False)
