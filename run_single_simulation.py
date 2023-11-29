import sys
"""
=========================
CHANGE THESE PATHS
=========================
"""
ANSYS_WIN64_PATH = "D:\Program Files\ANSYS\AnsysEM21.1\Win64\\"
ANSYS_PYTHON_PATH = "D:\Program Files\ANSYS\AnsysEM21.1\Win64\PythonFiles\DesktopPlugin\\"

sys.path.append(ANSYS_WIN64_PATH)
sys.path.append(ANSYS_PYTHON_PATH)

import ScriptEnv
import sys
import logging

# Initialize logging
logging.basicConfig(filename='single_simulation_log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the Electronics Desktop environment
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")

def run_simulation(uid, project_directory):
    try:
        project_path = os.path.join(project_directory, uid + ".aedt")
        oProject = oDesktop.OpenProject(project_path)
        oDesign = oProject.SetActiveDesign("CavitySweep_hfss")
        oDesign.Analyze("Setup")
        oProject.Save()
        oProject.Close()
        logging.info("Simulation completed for " + uid)
    except Exception as e:
        logging.error("Error in simulation for " + uid + ": " + str(e))

if __name__ == "__main__":
    uid = sys.argv[1]
    project_directory = sys.argv[2]
    run_simulation(uid, project_directory)