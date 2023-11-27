# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2021.1.0
# 14:07:10  Nov 27, 2023
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("clt_sweep_3830um_70um")
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
		"BasisOrder:="		, -1,
		"DoLambdaRefine:="	, True,
		"DoMaterialLambda:="	, True,
		"SetLambdaTarget:="	, False,
		"Target:="		, 0.4,
		"UseMaxTetIncrease:="	, False
	])
