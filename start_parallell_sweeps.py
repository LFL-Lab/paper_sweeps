# -*- coding: utf-8 -*-

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
import os
import subprocess
import time
import logging


"""
=========================  
PARAMETERS
=========================
"""

csv_path = PAPER_SWEEP_PATH + "project_storage\uids.csv"
project_path = os.path.dirname(csv_path)
ANSYS_PATH = ANSYS_WIN64_PATH + "ansysedt.exe"
PYTHON_EXE = ANSYS_WIN64_PATH + "common\IronPython\ipy64.exe"

num_sims = 3  # Number of simultaneous simulations
check_interval_mins = 60  # Time interval for checking simulation completion
completion_file_suffix = ".aedt.q.completed"  # Suffix for the completion check file


# Initialize logging
logging.basicConfig(filename=PAPER_SWEEP_PATH+'simulation_log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the Electronics Desktop environment
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")

"""
=========================  
FUNCTIONS
=========================
"""

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

# Function to check if a simulation is completed
def is_simulation_completed(uid, project_path, completion_file_suffix):
    return os.path.exists(os.path.join(project_path, uid + completion_file_suffix))

def run_ansys_simulation(uid, project_directory):
    try:
        oProject = oDesktop.SetActiveProject(uid)
        oDesign = oProject.SetActiveDesign("CavitySweep_hfss")  # Set the design name
        oDesign.Analyze("Setup")  # Set the setup name
        oProject.Save()
        oProject.Close()
        logging.info("Simulation completed for " + uid)
    except Exception as e:
        logging.error("Error in running simulation for " + uid + ": " + str(e))


# Function to display a simple progress bar
def print_progress(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    # print statement without f string
    print('\r%s |%s| %s%% %s \r' % (prefix, bar, percent, suffix))
    # Print New Line on Complete
    if iteration == total:
        print()


# Main function to manage simulations
def main(project_directory, num_sims, check_interval_mins, completion_file_suffix):
    project_files = [f for f in os.listdir(project_directory) if f.endswith('.aedt')]
    total_projects = len(project_files)
    projects_completed = 0

    active_sims = []
    for project_file in project_files:
        uid = os.path.splitext(project_file)[0]  # Extract UID from file name

        # Wait if maximum simulations are running
        while len(active_sims) >= num_sims:
            # Check for completed simulations
            completed_sims = [sim_uid for sim_uid in active_sims if
                              not is_simulation_completed(sim_uid, project_directory, completion_file_suffix)]
            for sim_uid in completed_sims:
                active_sims.remove(sim_uid)
                logging.info("Simulation completed for " + sim_uid)
                projects_completed += 1
                print_progress(projects_completed, total_projects, prefix='Progress:', suffix='Complete', length=50)
            time.sleep(check_interval_mins * 60)  # Check every specified minutes
        
        # Start a new simulation in a separate process
        subprocess.Popen([ANSYS_PATH, "-RunScript", "run_single_simulation.py", uid+".aedt", project_directory])
       # subprocess.Popen([PYTHON_EXE, "run_single_simulation.py", uid, project_directory])
        active_sims.append(uid)
        logging.info("Simulation started for " + uid + ".")

    # Wait for all simulations to complete
    while active_sims:
        completed_sims = [sim_uid for sim_uid in active_sims if
                          not is_simulation_completed(sim_uid, project_directory, completion_file_suffix)]
        for sim_uid in completed_sims:
            active_sims.remove(sim_uid)
            logging.info("Simulation completed for " + sim_uid)
            projects_completed += 1
            print_progress(projects_completed, total_projects, prefix='Progress:', suffix='Complete', length=50)
        time.sleep(check_interval_mins * 60)

    logging.info("All simulations completed.")

# Run the main function
main(project_path, num_sims, check_interval_mins, completion_file_suffix)