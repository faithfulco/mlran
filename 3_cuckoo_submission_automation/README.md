## Submit folder

This custom script automates the process of submitting files to Cuckoo Sandbox for analysis. Using this script, you can efficiently submit multiple files one after the other, ensuring that each submission is spaced out to prevent any potential clashes or overloads in the analysis system. The cuckoo documentation https://cuckoo.readthedocs.io/en/latest/usage/submit/ contains a method for submitting a folder for analysis and the files would be analysed one after the other. However, when applied it often leads the system to crash. So, it's necessary to develop this custom simple script to automate the process and avoid the crash. 

## Extraction folder

This script automates the extraction of key files generated by Cuckoo Sandbox after an analysis task is completed. It ensures that the necessary files are organized into specific directories for easy access and further processing.

The script performs the following actions:
1. Extracts the **binary**, **report.json**, **stats.log**, and **raw zipped results**.
2. Organizes the files into pre-defined directories.
3. Gracefully handles errors by skipping file extraction if an error (matching the error pattern specified in the script) is detected during the analysis.
4. Logs the extraction process for monitoring and debugging purposes.
