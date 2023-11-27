# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2021.1.0
# 14:21:48  Nov 27, 2023
# ----------------------------------------------
import ScriptEnv
import os
import csv

ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")

oDesktop.RestoreWindow()


oProject = oDesktop.SetActiveProject(uid)
oProject.Save()
oDesign = oProject.SetActiveDesign("CavitySweep_hfss")
oDesign.Analyze("Setup")
oProject.Save() #might not work