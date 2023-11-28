import sys

ANSYS_WIN64_PATH = "D:\Program Files\ANSYS\AnsysEM21.1\Win64\\"
ANSYS_PYTHON_PATH = "D:\Program Files\ANSYS\AnsysEM21.1\Win64\PythonFiles\DesktopPlugin\\"

sys.path.append(ANSYS_WIN64_PATH)
sys.path.append(ANSYS_PYTHON_PATH)

import ScriptEnv
import os

# Initialize the Electronics Desktop environment
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop = ScriptEnv.GetDesktop()

# Specify the directory containing the Ansys project files
project_directory = r"d:\andre\paper_sweeps\project_storage"  # Update this path as needed

# List all Ansys project files in the directory
project_files = [f for f in os.listdir(project_directory) if f.endswith('.aedt')]

# Open each project
for project_file in project_files:
    project_path = os.path.join(project_directory, project_file)
    oDesktop.OpenProject(project_path)
    print("Opened project: " + project_file)

def remove_lock_files(project_path):
    # Construct the pattern to match all '.lock' files
    lock_files_pattern = os.path.join(project_path, '*.lock')

    # Use glob to find all files in the directory that end with '.lock'
    lock_files = glob.glob(lock_files_pattern)

    # Iterate over the list of file paths & remove each file
    for lock_file in lock_files:
        try:
            os.remove(lock_file)
            print(f"Deleted: {lock_file}")
        except OSError as e:
            print(f"Error: {e.strerror} - {lock_file}")

remove_lock_files(project_path)