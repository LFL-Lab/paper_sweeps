# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2021.1.0
# 14:07:10  Nov 27, 2023
# ----------------------------------------------
import ScriptEnv
import os
import csv

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
	oProject.Save() #might not work