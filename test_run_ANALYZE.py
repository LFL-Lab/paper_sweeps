# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2021.1.0
# 16:41:03  Nov 28, 2023
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("Saruman_clt_sweep_3830um_205um_255um")
oProject.Save()
oDesign = oProject.SetActiveDesign("CavitySweep_hfss")
oDesign.Analyze("Setup")
oProject = oDesktop.SetActiveProject("Saruman_clt_sweep_3830um_220um_225um")
oProject.Save()
oDesign = oProject.SetActiveDesign("CavitySweep_hfss")
oDesign.Analyze("Setup")
