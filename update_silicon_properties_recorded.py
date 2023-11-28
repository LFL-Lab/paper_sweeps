# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2021.1.0
# 12:38:05  Nov 28, 2023
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("clt_sweep_3830um_325um_240um")
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
