# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2021.1.0
# 15:42:01  Nov 27, 2023
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("clt_sweep_3900um_215um")
oDesign = oProject.SetActiveDesign("CavitySweep_hfss")
oDesign.Analyze("Setup")
oProject = oDesktop.SetActiveProject("clt_sweep_3830um_90um")
oProject.Save()
oDesign = oProject.SetActiveDesign("CavitySweep_hfss")
oDesign.Analyze("Setup")
oProject = oDesktop.SetActiveProject("clt_sweep_3830um_80um")
oProject.Save()
oDesign = oProject.SetActiveDesign("CavitySweep_hfss")
oDesign.Analyze("Setup")
oProject = oDesktop.SetActiveProject("clt_sweep_3830um_70um")
oProject.Save()
oDesign = oProject.SetActiveDesign("CavitySweep_hfss")
oDesign.Analyze("Setup")
