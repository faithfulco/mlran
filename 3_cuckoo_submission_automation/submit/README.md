# Cuckoo File Submission Automation Script

## Overview

This custom script automates the process of submitting files to Cuckoo Sandbox for analysis. Using this script, you can efficiently submit multiple files one after the other, ensuring that each submission is spaced out to prevent any potential clashes or overloads in the analysis system. The cuckoo documentation https://cuckoo.readthedocs.io/en/latest/usage/submit/ contains a method for submitting a folder for analysis and the files would be analysed one after the other. However, when applied it often leads the system to crash. So, it's necessary to develop this custom simple script to automate the process and avoid the crash. 

## Importance of This Code

Automating the file submission process to Cuckoo Sandbox provides several benefits:

1. **Efficiency**: Submitting files manually can be time-consuming, especially if you have a large number of files to analyze. This script streamlines the process, allowing you to focus on interpreting the results rather than handling the logistics of submission.

2. **Consistency**: The script ensures that each file is submitted with a consistent delay between submissions, which can help in avoiding performance issues that may arise from submitting multiple files at once.

3. **Reliability**: By preventing system hibernation, the script minimizes the risk of interruptions during the submission process, allowing for a smoother workflow.

## Prerequisites

Before running the script, ensure that you have the following:

- **Cuckoo Sandbox**: Installed and configured on your system.
- **Python 2.7**: Ensure Python 2.7 is available in your environment.
- **Access to Terminal**: You will need to use the terminal to run the script and submit files.

## Setup Instructions

1. **Prevent System Hibernation**: To prevent your computer from going into hibernation during the file submission process, run the following command in your terminal:

   ```bash
   sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
   ```

2. **Prepare Your Files**: Organize the files you want to analyze into a designated folder. For example, you can place all your files in:

   ```
   FOLDER_PATH = '/home/user/Downloads/Wares'
   ```

   You can include multiple files, such as 50 or more, in the `Wares` folder.

3. **Start Cuckoo**: Launch Cuckoo Sandbox using your preferred method, ensuring it is set up to handle the analysis. You can open multiple terminal sessions (e.g., using Terminator) to run the necessary Cuckoo processes.

4. **Download the Script**: Download the submission script to your Downloads folder. Make sure the script is named `submit_cuckoo_main.py`.

5. **Activate the Cuckoo Environment**: In the terminal where Cuckoo is running, activate your Cuckoo virtual environment:

   ```bash
   workon <cuckoo_env>
   ```

6. **Run the Script**: Execute the following command in the terminal:

   ```bash
   python2 submit_cuckoo_main.py
   ```

7. **Testing**: For initial testing, it is recommended to use a smaller batch of files (e.g., 10 files) from your `Wares` folder to ensure the script functions as expected.

## Conclusion

This script serves as a valuable tool for automating the submission of files to Cuckoo Sandbox, allowing for a more efficient and reliable analysis workflow. By following the instructions provided, you can streamline the process of malware analysis and focus on gaining insights from the results.



# Missing Files Report - `missing_files.py`

This Python 2.7 script checks for missing `.json` files in a specified range within a given folder and generates a CSV report listing the missing file numbers.

## Features:
- **Check for Missing Files**: The script scans a folder for files named in a numeric sequence (e.g., `13001.json`, `13002.json`) and identifies missing files in the specified range.
- **CSV Report**: It creates a `missing_files.csv` file, listing all missing file numbers.

## Usage:
1. **Set the folder path** where the `.json` files are stored (default is `/home/user/Downloads/Uploads/Reports`).
   
2. **Adjust the file range** by modifying the `start_range` and `end_range` in the `main()` function.

3. **Run the script**:
   ```bash
   python2 missing_files.py
   ```

4. **Output**: A CSV file named `missing_files.csv` will be generated, containing the missing file numbers.

## Example:
If files `13001.json`, `13002.json`, and `13003.json` are present but `13004.json` is missing, the CSV will list `13004`.

## Requirements:
- Python 2.7
- CSV files

This script helps ensure all expected files are accounted for in batch processing scenarios.
