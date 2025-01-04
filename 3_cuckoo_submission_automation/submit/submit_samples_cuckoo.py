import os
import time
import subprocess

# Folder containing the files for analysis
FOLDER_PATH = '/home/user/Downloads/Wares'  # Path to your samples folder

def submit_file_to_cuckoo(file_path):
    """Submit a file to Cuckoo Sandbox for analysis using the command line."""
    command = [ 'cuckoo', 'submit', 
	'--timeout', '120', 
	'--options', 'procmemdump=yes,route=internet', 
	file_path ]
    
    try:
        # Execute the command
        subprocess.check_call(command)
        print("File {} submitted successfully.".format(file_path))
    except subprocess.CalledProcessError as e:
        print("Failed to submit {}. Error: {}".format(file_path, e))

def main():
    # List all files in the specified folder
    files = [os.path.join(FOLDER_PATH, f) for f in os.listdir(FOLDER_PATH) if os.path.isfile(os.path.join(FOLDER_PATH, f))]
    
    for file_path in files:
        # Submit file for analysis
        submit_file_to_cuckoo(file_path)
        
        # Wait for 5 minutes before submitting the next file
        print("Waiting for 5 minutes before submitting the next file...")
        time.sleep(6 * 60)  # 5 minutes in seconds

if __name__ == "__main__":
    main()
