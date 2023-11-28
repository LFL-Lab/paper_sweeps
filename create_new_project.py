"""Create a new project"""
import sys


sys.path.append(ANSYS_WIN64_PATH)
sys.path.append(ANSYS_PYTHON_PATH)
sys.path.append(PAPER_SWEEP_PATH)

import ScriptEnv
import csv
import os
from utils import remove_lock_files

# Initialize the Electronics Desktop environment
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")

# Specify the CSV file path
csv_path = r"d:\Andre\paper_sweeps\project_storage\uids.csv" #UPDATE THIS
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