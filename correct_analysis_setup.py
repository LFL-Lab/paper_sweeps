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
            print("Deleted: " + "lock_file")
        except OSError as e:
            print("Error: %s - %s." % (e.strerror, lock_file))

ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()

# Specify the CSV file path
CSV_PATH = r"d:\andre\paper_sweeps\project_storage\uids.csv" #UPDATE THIS
project_path = os.path.dirname(CSV_PATH)

# Read the UIDs from the CSV file
uids = []

# Open the CSV file and read the UIDs
csvfile = open(CSV_PATH, 'r')
csv_reader = csv.reader(csvfile)
header = next(csv_reader)  # Skip the header
for row in csv_reader:
    uids.append(row[0])  # Assuming the UID is in the first column
csvfile.close()  # Close the CSV file

# Create new projects with names based on the UID
for uid in uids:
	# Define the full path for the new project using the UID
	print(50*"=")
	print("Updating the Setup for " + uid + "\n")
	oProject = oDesktop.SetActiveProject(uid)
	oDesign = oProject.SetActiveDesign("CavitySweep_hfss")
	oModule = oDesign.GetModule("AnalysisSetup")
	oModule.EditSetup("Setup", 
		[
			"NAME:Setup",
			"MinimumFrequency:="	, "1GHz",
			"NumModes:="		, 1,
			"MaxDeltaFreq:="	, 0.05,
			"ConvergeOnRealFreq:="	, True,
			"MaximumPasses:="	, 30,
			"MinimumPasses:="	, 2,
			"MinimumConvergedPasses:=", 1,
			"PercentRefinement:="	, 30,
			"IsEnabled:="		, True,
			[
				"NAME:MeshLink",
				"ImportMesh:="		, False
			],
			"BasisOrder:="		, 1,
			"DoLambdaRefine:="	, True,
			"DoMaterialLambda:="	, True,
			"SetLambdaTarget:="	, False,
			"Target:="		, 0.4,
			"UseMaxTetIncrease:="	, False
		])
	
	print("Fixing the material properties of ultracold Si for " + uid)
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
	print(50*"=")
	print("\n\n")
	oProject.Save()

remove_lock_files(project_path)