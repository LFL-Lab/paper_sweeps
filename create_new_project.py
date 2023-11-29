"""Create a new project"""
import sys
"""
=========================
CHANGE THESE PATHS
=========================
"""
PAPER_SWEEP_PATH = "D:\Andre\paper_sweeps\\"
ANSYS_WIN64_PATH = "D:\Program Files\ANSYS\AnsysEM21.1\Win64\\"
ANSYS_PYTHON_PATH = "D:\Program Files\ANSYS\AnsysEM21.1\Win64\PythonFiles\DesktopPlugin\\"

sys.path.append(ANSYS_WIN64_PATH)
sys.path.append(ANSYS_PYTHON_PATH)
sys.path.append(PAPER_SWEEP_PATH)

import ScriptEnv
import csv
import os
import glob

def remove_lock_files(project_path):
    # Construct the pattern to match all '.lock' files
    lock_files_pattern = os.path.join(project_path, '*.lock')

    # Use glob to find all files in the directory that end with '.lock'
    lock_files = glob.glob(lock_files_pattern)

    # Iterate over the list of file paths & remove each file
    for lock_file in lock_files:
        try:
            os.remove(lock_file)
            print("Deleted: " + lock_file)
        except OSError as e:
            print("Error: %s - %s." % (e.strerror, lock_file))

# Initialize the Electronics Desktop environment
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")

# Specify the CSV file path
csv_path = PAPER_SWEEP_PATH + "project_storage\uids.csv"
project_path = os.path.dirname(csv_path)

# Read the UIDs from the CSV file
uids = []

# Open the CSV file and read the UIDs
csvfile = open(csv_path, 'r')
csv_reader = csv.reader(csvfile)
header = next(csv_reader)  # Skip the header
for row in csv_reader:
    uids.append(row[0])  # Assuming the UID is in the first column
csvfile.close()  # Close the CSV file

# Create new projects with names based on the UID
for uid in uids:
    # Define the full path for the new project using the UID
    uid+=".aedt"
    project_full_path = os.path.join(project_path, uid)
    oDesktop.RestoreWindow()
    oProject = oDesktop.NewProject(project_full_path)
    oProject.SaveAs(project_full_path, True)

remove_lock_files(project_path)