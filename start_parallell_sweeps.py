import ScriptEnv
import os
import csv
import time

ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()

# Function to start a simulation for a given UID
def start_simulation(uid, project_path, design_name, setup_name):
    try:
        oProject = oDesktop.SetActiveProject(uid)
        oDesign = oProject.SetActiveDesign(design_name)
        oDesign.Analyze(setup_name)
        print("Simulation started for " + uid + ".")
    except Exception as e:
        print("Error in starting simulation for " + uid + ": " + str(e))

# Function to check if a simulation is completed
def is_simulation_completed(uid, project_path):
    return os.path.exists(os.path.join(project_path, uid + ".aedt.q.completed"))

# Function to save and close a project
def save_and_close_project(uid, project_path):
    try:
        oProject = oDesktop.OpenProject(os.path.join(project_path, uid + ".aedt"))
        oProject.Save()
        oProject.Close()
        print("Project for " + uid + " saved and closed.")
    except Exception as e:
        print("Error in saving and closing project for " + uid + ": " + str(e))

# Main function to control the simulation queue
def main(csv_path, num_sims, design_name, setup_name, wait_time_mins):
    project_path = os.path.dirname(csv_path)
    uids = []

    # Read UIDs from the CSV file
    with open(csv_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip the header
        for row in csv_reader:
            uids.append(row[0])

    # Iterate over UIDs and manage simulation queue
    active_sims = []
    for uid in uids:
        if len(active_sims) < num_sims:
            start_simulation(uid, project_path, design_name, setup_name)
            active_sims.append(uid)
        else:
            while len(active_sims) >= num_sims:
                for sim_uid in active_sims[:]:
                    if is_simulation_completed(sim_uid, project_path):
                        save_and_close_project(sim_uid, project_path)
                        active_sims.remove(sim_uid)
                        print("Simulation for " + sim_uid + " completed.")
                time.sleep(wait_time_mins * 60)  # Check every specified minutes

    # Wait for the remaining simulations to complete
    while active_sims:
        for sim_uid in active_sims[:]:
            if is_simulation_completed(sim_uid, project_path):
                save_and_close_project(sim_uid, project_path)
                active_sims.remove(sim_uid)
                print("Simulation for " + sim_uid + " completed.")
        time.sleep(wait_time_mins * 60)  # Check every specified minutes

    print("All simulations completed.")

# Specify the parameters
csv_path = r"d:\andre\paper_sweeps\project_storage\uids.csv"  # UPDATE THIS
num_sims = 3  # UPDATE THIS
design_name = "CavitySweep_hfss"  # UPDATE THIS IF NEEDED
setup_name = "Setup"  # UPDATE THIS IF NEEDED
wait_time_mins = 20  # UPDATE THIS IF NEEDED

# Run the main function
main(csv_path, num_sims, design_name, setup_name, wait_time_mins)