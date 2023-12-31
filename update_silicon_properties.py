# ----------------------------------------------
# Purpose:
#	 1. Sets the Analysis Setup
# 	2. Changes Si material properties
# ----------------------------------------------
import sys

PAPER_SWEEP_PATH = "D:\Andre\paper_sweeps\\"
ANSYS_WIN64_PATH = "D:\Program Files\ANSYS\AnsysEM21.1\Win64\\"
ANSYS_PYTHON_PATH = "D:\Program Files\ANSYS\AnsysEM21.1\Win64\PythonFiles\DesktopPlugin\\"

sys.path.append(ANSYS_WIN64_PATH)
sys.path.append(ANSYS_PYTHON_PATH)
sys.path.append(PAPER_SWEEP_PATH)

import ScriptEnv
import os
import csv
from utils import remove_lock_files


ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()

# Specify the CSV file path
csv_path = r"d:\andre\paper_sweeps\project_storage\uids.csv" #UPDATE THIS
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
    #print("Updating the Setup for " + uid + "\n")
    oProject = oDesktop.SetActiveProject(uid)
    oDesign = oProject.SetActiveDesign("CavitySweep_hfss")
    oDefinitionManager = oProject.GetDefinitionManager()
    oDefinitionManager.EditMaterial("silicon", 
        [
            "NAME:silicon",
            "CoordinateSystemType:=", "Cartesian",
            "BulkOrSurfaceType:="	, 1,
            [
                "NAME:PhysicsTypes",
                "set:="			, ["Electromagnetic","Thermal","Structural"]
            ],
            [
                "NAME:AttachedData",
                [
                    "NAME:MatAppearanceData",
                    "property_data:="	, "appearance_data",
                    "Red:="			, 89,
                    "Green:="		, 94,
                    "Blue:="		, 107
                ]
            ],
            "permittivity:="	, "11.45",
            "dielectric_loss_tangent:=", "1e-07",
            "thermal_conductivity:=", "148",
            "mass_density:="	, "2330",
            "specific_heat:="	, "712",
            "youngs_modulus:="	, "135000000000",
            "poissons_ratio:="	, "0.25",
            "thermal_expansion_coefficient:=", "2.54e-06"
        ])
    print("Silicon material properties updated.")
    oProject.Save()

remove_lock_files(project_path)