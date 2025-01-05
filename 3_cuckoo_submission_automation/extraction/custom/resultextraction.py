import os
import re
import json
import io
import zipfile
import shutil
import traceback
import logging

from cuckoo.common.utils import json_default
from cuckoo.web.controllers.analysis.analysis import AnalysisController

log = logging.getLogger(__name__)

# Define the paths to the main directory
parent_directory = os.path.expanduser("~/Downloads/Uploads")

# Define the path to the full zipped result when the full_zip_result function is used
zipped_result_path = os.path.dirname(parent_directory)

# Define the paths to target output directories
output_binary_directory = os.path.join(parent_directory, "Binaries")
output_report_directory = os.path.join(parent_directory, "Reports")
output_stats_directory = os.path.join(parent_directory,  "Stats")
output_raw_result_zip_directory = os.path.join(parent_directory,  "RawResults")

# Define the path, relative to the task_id folder, to the file to be extracted (file pointer)
path_to_binary = "binary"
path_to_stats_file = os.path.join("suricata", "stats.log")
path_to_report_file = os.path.join("reports", "report.json")
path_to_the_zip_file = ""

# Dictionary to combine the input and output parts for easy access
extraction_list = [
			{"input_path":path_to_binary, "output_path":output_binary_directory},
			{"input_path":path_to_stats_file, "output_path":output_stats_directory},
			{"input_path":path_to_report_file, "output_path":output_report_directory},
			{"input_path":path_to_the_zip_file, "output_path":output_raw_result_zip_directory}
			
		  ]


pattern = r"Cuckoo\w*Error"

class ResultExtraction():
    '''
       Rename and Extract the following into the required directory:
       	1. Binary
       	2. stats.log
       	3. report.json
       	4. The zip archive of the whole result
    '''
    
            
    _report = None
    _analysis_path = ""
    _original_filename = ""
            
    @classmethod
    def check_for_error(cls, task_id):
    
        log.info("Checking for possible error(s) during and after the analysis")
        
        error_found = False
        cuckoo_log_file_path = os.path.join(cls._analysis_path, "cuckoo.log")
        
        with open(cuckoo_log_file_path, 'r') as f:
            #for line in f:
            #    if any(x in line for x in ["ERROR:", "/status failed."]) or re.search(pattern, line):
            for line_number,  line in enumerate(f, 1):
                if re.search(r'\berror\b:?', line, re.IGNORECASE) and "WARNING: Error" not in line and "Error dumping file from path" not in line and "ERROR: Failed to run 'on_call'" not in line and "Error returned by is32bit" not in line:
                    error_found = True
                    log.info("Error found for Task #%d. No file was extracted", task_id)
                    break            
        return error_found
        
 
    @classmethod
    def get_full_result_in_zip_archive(cls, task_id, result_path=None):
        
        log.info("Getting Task #%d report into a zip archive", task_id)
        
        #check for error
        #ret = cls.check_for_error(task_id)
        #if ret is True:
        #    return
            
        report = cls._report
        analysis_path = cls._analysis_path
        original_filename = cls._original_filename
        
        if result_path == None:
           result_path = zipped_result_path
   
        # Define path for the exported result
        path = os.path.join(result_path, original_filename + '.zip')
        if os.path.exists(path):
            os.remove(path)
     
        try:
          
            f = io.BytesIO()
            z = zipfile.ZipFile(f, "w", zipfile.ZIP_DEFLATED, allowZip64=True)

            for dirpath, dirnames, filenames in os.walk(analysis_path):
                if os.path.basename(dirpath) == str(task_id):
                    for filename in filenames:
                        z.write(os.path.join(dirpath, filename), filename)
                        
                if os.path.basename(dirpath) != str(task_id):
                    for filename in filenames:
                        z.write(
                            os.path.join(dirpath, filename),
                            os.path.join(os.path.basename(dirpath), filename)
                        )

            # Creating an analysis.json file with additional information about this
            # analysis. This information serves as metadata when importing a task.
            obj = {
                "action": report.get("debug", {}).get("action", []),
                "errors": report.get("debug", {}).get("errors", []),
            }
            z.writestr(
                "analysis.json", json.dumps(obj, indent=4, default=json_default)
            )

            z.close()

            with open(path, 'wb') as f_out:
                f_out.write(f.getvalue())

            f.close()

            return 
        except Exception as e:
            print(traceback.format_exc())
            print("Error: {}".format(e))
            
            
    @classmethod
    def extractfiles(cls, task_id):
        
        cls._report = AnalysisController.get_report(task_id)
        cls._report = cls._report["analysis"]
        cls._analysis_path = cls._report["info"]["analysis_path"]
        cls._original_filename = os.path.splitext(cls._report['target']['file']['name'])[0]
        
        log.info("Extracting the necessary files from %s (Task #%d) Report", cls._original_filename, task_id)
        
        analysis_path = cls._analysis_path
        original_filename = cls._original_filename
        
        #check for error
        ret = cls.check_for_error(task_id)
        if ret is True:
            return
        
        for dic in extraction_list:
            for dirpath, dirnames, filenames in os.walk(analysis_path):
                current_path = os.path.normpath(os.path.join(analysis_path, dic['input_path']))
                
                if os.path.exists(current_path) and current_path != analysis_path:
                    extension = os.path.splitext(dic['input_path'])[1]
                    copy_path = os.path.join(dic['output_path'], original_filename+extension)
                    
                    if os.path.exists(copy_path):
                        os.remove(copy_path)
                    shutil.copy(current_path, copy_path)
                    
                    if dic['input_path'] == "binary":
                        output = os.path.join(dic['output_path'], "{}.zip".format(original_filename))
        
                        with zipfile.ZipFile(output, 'w') as zf:
                            zf.write(copy_path, arcname=os.path.basename(original_filename))
                        os.remove(copy_path)
                    break
                    
                elif current_path == analysis_path:
                    cls.get_full_result_in_zip_archive(task_id, dic['output_path'])
                    try:
                        directory = os.path.expanduser('~/Downloads/Wares/Ransomwares')
                        os.remove(os.path.join(directory, original_filename))
                    except Exception as e:
                        print(e)
                    break
                    
        log.info("Extraction of the necessary files from %s was successful", original_filename)
                    
                    
    
