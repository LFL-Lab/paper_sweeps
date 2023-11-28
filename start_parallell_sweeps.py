import sys

ANSYS_WIN64_PATH = "D:\Program Files\ANSYS\AnsysEM21.1\Win64\\"
ANSYS_PYTHON_PATH = "D:\Program Files\ANSYS\AnsysEM21.1\Win64\PythonFiles\DesktopPlugin\\"

sys.path.append(ANSYS_WIN64_PATH)
sys.path.append(ANSYS_PYTHON_PATH)

import ScriptEnv
import os
import subprocess
import time
import logging
from tqdm import tqdm

# Initialize logging
logging.basicConfig(filename='simulation_log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the Electronics Desktop environment
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop = ScriptEnv.GetDesktop()


# Function to check if a simulation is completed
def is_simulation_completed(uid, project_path, completion_file_suffix):
    return os.path.exists(os.path.join(project_path, uid + completion_file_suffix))


# Main function to manage simulations
def main(project_directory, num_sims, check_interval_mins, completion_file_suffix):
    project_files = [f for f in os.listdir(project_directory) if f.endswith('.aedt')]

    with tqdm(total=len(project_files)) as pbar:
        active_sims = []
        for project_file in project_files:
            project_path = os.path.join(project_directory, project_file)
            uid = os.path.splitext(project_file)[0]  # Extract UID from file name

            # Wait if maximum simulations are running
            while len(active_sims) >= num_sims:
                completed_sims = [sim_uid for sim_uid in active_sims if
                                  not is_simulation_completed(sim_uid, project_directory, completion_file_suffix)]
                for sim_uid in completed_sims:
                    active_sims.remove(sim_uid)
                    logging.info(f"Simulation completed for {sim_uid}")
                    pbar.update(1)
                time.sleep(check_interval_mins * 60)  # Check every specified minutes

            # Start a new simulation
            subprocess.Popen(["C:\\path\\to\\ansysedt.exe", "-RunScriptAndExit", project_path])
            active_sims.append(uid)
            logging.info(f"Simulation started for {uid}")

        # Wait for all simulations to complete
        while active_sims:
            completed_sims = [sim_uid for sim_uid in active_sims if
                              not is_simulation_completed(sim_uid, project_directory, completion_file_suffix)]
            for sim_uid in completed_sims:
                active_sims.remove(sim_uid)
                logging.info(f"Simulation completed for {sim_uid}")
                pbar.update(1)
            time.sleep(check_interval_mins * 60)

        logging.info("All simulations completed.")


# Parameters
project_directory = r"D:\path\to\project\files"  # Update this path
num_sims = 3  # Number of simultaneous simulations
check_interval_mins = 20  # Time interval for checking simulation completion
completion_file_suffix = ".aedt.q.completed"  # Suffix for the completion check file

# Run the main function
main(project_directory, num_sims, check_interval_mins, completion_file_suffix)