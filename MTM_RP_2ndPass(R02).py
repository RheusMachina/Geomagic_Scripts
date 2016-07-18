import geomagic.app.v2
for m in geomagic.app.v2.execStrings: exec m in locals(), globals()
import os,time,subprocess,shutil,datetime,math
#
#File Folder Location
Terminal = u'C:\\Users\\Public\\Documents\MTM Automation\\'
#
#Working Folders===================================================================================
savePath = Terminal + 'RP_Automation\\C_3rdPass_Input\\'
rawPath = Terminal + 'RP_Automation\\RAW\\'
path_to_watch = Terminal + 'RP_Automation\\B_2ndPass_Input\\'
#====================================================================================================
if not os.path.exists(savePath): os.makedirs(savePath)
if not os.path.exists(rawPath): os.makedirs(rawPath)
x=[] #Empty list to allow user to break out of script running...add a file called "done.txt" to Watch Folder to end script
#======================================================================================================================================================================
#
#Define Function Sub Routines==========================================================================================================================================
#======================================================================================================================================================================
#Save Context===================================================================================
__saved_context__ = {}
def saveContext():
    import sys
    __saved_context__.update(sys.modules[__name__].__dict__)
#Restore Context=================================================================================
def restoreContext():
    import sys
    names = sys.modules[__name__].__dict__.keys()
    for n in names:
        if n not in __saved_context__:
            del sys.modules[__name__].__dict__[n]
#Disable Display================================================================================
def dispOff():
	print 'DISPLAY OFF'
	geo.set_option("Graphics/Disable Display", 1)
#Enable Display=================================================================================
def dispOn():
	print 'DISPLAY ON'
	geo.set_option("Graphics/Disable Display", 0)
#Object Open=================================================================================
def GetFile(fto):
	geo.open(0,1,fto)
#Object Duplicate=================================================================================
def dupObj():
	activeModel = geoapp.getActiveModel()
	originalMesh = geoapp.getMesh(activeModel)
	duplicate = Duplicate()
	duplicate.object = originalMesh
	duplicate.run()
	mesh = duplicate.clonedobject
	geoapp.deleteModel( originalMesh )
	return mesh
#Object Add =================================================================================
def RetObj(fMesh, cnum):
	tempMesh = Mesh()
	merger = MergeMeshes()
	merger.mesh = tempMesh
	merger.meshModelAdd = fMesh
	merger.run()
	tempMesh.name = cnum
	geoapp.addModel( tempMesh, tempMesh.name )
#Object Y================================================================================
def yloc():
	model = geoapp.getActiveModel()
	mesh = geoapp.getMesh(model)
	analyzer = Analyze(mesh)
	analyzer.run()
	cg = str(analyzer.centerOfGravity).split(",")
	return float(cg[1])
#Object Z================================================================================
def zloc():
	model = geoapp.getActiveModel()
	mesh = geoapp.getMesh(model)
	analyzer = Analyze(mesh)
	analyzer.run()
	cg = str(analyzer.centerOfGravity).split(",")
	cg = cg[2].split(")")
	return float(cg[0])
#Volume Check================================================================================
def volcheck():
	model = geoapp.getActiveModel()
	mesh = geoapp.getMesh(model)
	analyzer = Analyze(mesh)
	analyzer.run()
	volc = analyzer.volume * 1000000
	return volc
#Volume Correct================================================================================
def volcorrect():
	vols = 0
	i = 0
	while i < 15:
		vols = volcheck()
		if vols < 1:
			if i == 0: cleanMesh(-0.05,1,1)
			geo.exact_position(0,-0.00025,0,0,0,0,1,0,0,1)
			geo.section_by_plane(1,0,1,1,0,1,0,-0.003,0)
			geo.make_open_manifold()
			i+=1
		else:
			i=15
#Case Model Alignments================================================================================
def BFA2(rnum, tnum, o1):
	#0 = Mand 1 = Max 2 = OCC
	geo.select_objects(1, "Polygon", 1, tnum)
	model = geoapp.getActiveModel()	
	geoapp.setNamedReferenceModel("TestObject",model)
	geo.select_objects(1, "Polygon", 1, rnum)
	model = geoapp.getActiveModel()
	geoapp.setNamedReferenceModel("RefObject",model)
	cy = yloc()
	cz = zloc()
	if o1 == 0:
		cz1 = -0.15
		cz2 = 0.15
		cy1 = cy
		cy2 = cy + 0.05
	elif o1 == 1:
		cz1 = -0.15
		cz2 = 0.15
		cy1 = cy
		cy2 = cy - 0.05
	elif o1 == 2:
		cy1 = cy + 0.010
		cy2 = cy - 0.010
		cz1 = cz + 0.01
		cz2 = cz - 0.07
		geo.select_objects(1, "Polygon", 2, tnum, rnum)
	geo.select_volume(-0.05, cy1, cz1, 0.05, cy2, cz2)
	for shi in range (0,3):
		geo.shrink_selection_multi()
	geo.select_objects(1, "Polygon", 1, tnum)
	geo.qual_best_fit_alignment(-1, 300, 0.00025, 0, 1, 0, 0, 20, 0, 1, 0, 0, -1)
	if o1 != 2:
		geo.select_objects(1, "Polygon", 1, tnum)
		geo.select_volume(-0.05, cy1, cz1, 0.05, cy2, cz2)
		for shi in range (0,3):
			geo.shrink_selection_multi()
	geo.qual_best_fit_alignment(-1, 900, 0.00025, 0, 1, 1, 1, 10, 0, 1, 0, 0, -1)
	geo.qual_best_fit_alignment(-1, 1500, 0.00025, 0, 1, 1, 1, 5, 0, 1, 0, 0, -1)
	geo.select_objects(1, "Polygon", 2, rnum, tnum)
	geo.select_all()
	geo.clear_all()
#Merge Models================================================================================
def occ(unum, lnum, num):
	geo.select_objects(1, "Polygon", 2, unum, lnum)
	geo.select_all()
	geo.clear_all()
	geo.boolean_operations(num, 0, 0, 1, 0, 0, 0, 0, 0, 0)
#Overlay Models================================================================================
def Overlay(numI, numF, numO):
	#Set Test Model Based off Selection=========
	geo.select_objects(1, "Polygon", 1, numI)
	model = geoapp.getActiveModel()
	geoapp.setNamedReferenceModel("TestObject",model)
	#Set REF Model Based off Selection==========
	geo.select_objects(1, "Polygon", 1, numF)
	model = geoapp.getActiveModel()
	geoapp.setNamedReferenceModel("RefObject", model)
	cgz = zloc()
	#Best Fit Alignment=============
	geo.select_objects(1, "Polygon", 2, numF, numI)
	geo.select_volume(-0.05, 0, -0.05, 0.05, 0.05, 0.15)
	geo.select_objects(0, "TestObject", 0)
	geo.qual_best_fit_alignment(-1, 300, 0.002, 0, 1, 0, 0, 100, 0, 1, 0, 0, -1)
	geo.select_objects(1, "Polygon", 2, numF, numI)
	geo.select_volume(-0.05, 0.002, -0.05, 0.05, 0.05, cgz)
	geo.select_objects(0, "TestObject", 0)
	geo.qual_best_fit_alignment(-1, 900, 0.00015, 0, 1, 1, 1, 100, 0, 1, 0, 0, -1)
	geo.qual_best_fit_alignment(-1, 1500, 0.00015, 0, 1, 1, 1, 100, 0, 1, 0, 0, -1)
	geo.qual_best_fit_alignment(-1, 4500, 0.0005, 0, 1, 1, 1, 100, 0, 1, 0, 0, -1)
	geo.select_objects(1, "Polygon", 2, numF, numI)
	geo.select_all()
	geo.clear_all()
	geo.section_by_plane(1, 0, 1, 1, -0, -0, -1, -0, 0)
	geo.boolean_operations(numO, 0, 0, 1, 0, 0, 0, 0, 1, 0)
#MeshCleaning================================================================================
def cleanMesh(rmy, rmc, rmd):
	geo.select_volume(-0.05, 0.0005, -0.1, 0.05, rmy, 0.1)
	if rmc == 1: geo.remesh(0.0003, 1, 0, 180, 0.003, 1, 0, 0, 0.0003, 0)
	geo.remove_spikes_new(100)
	geo.relax_polygons(50, 0, 1, -1, 3)
	if rmd == 1:geo.mesh_doctor("smallcompsize", 0, "smalltunnelsize", 0, "holesize", 0, "spikesens", 50, "spikelevel", 0.5, "defeatureoption", 2, "fillholeoption", 2, "autoexpand", 2, "operations", "IntersectionCheck+", "SmallComponentCheck+", "SpikeCheck+", "HighCreaseCheck+", "Update", "Auto-Repair")
	geo.select_all()
	geo.clear_all()
#Base Extrude================================================================================
def baseExt(numI, numF):
	baseF = numF + "-2"
	baseI = numI + "-2"
	geo.select_objects(1, "Polygon", 1, numF)
	cleanMesh(-0.0005,0,0)
	Fmesh2b = dupObj()
	RetObj(Fmesh2b,numF)
	geo.section_by_plane(1, 0, 1, 0, -0, -1, -0, -0, 0)
	RetObj(Fmesh2b,baseF)
	geo.section_by_plane(1, 1, 1, 0, -0, -1, -0, -0, 0)
	geo.select_objects(1, "Polygon", 1, numI)
	cleanMesh(-0.0005,0,0)
	Imesh2b = dupObj()
	RetObj(Imesh2b,numI)
	geo.section_by_plane(1, 0, 1, 0, -0, -1, -0, -0, 0)
	RetObj(Imesh2b,baseI)
	geo.section_by_plane(1, 1, 1, 0, -0, -1, -0, -0, 0)
	geo.select_objects(1, "Polygon", 1, baseF)
	geo.scale_model(1, 1, 1, 21, 1, 0, 0, 20, 1, 0, 1)
	geo.select_objects(1, "Polygon", 2, baseF, numF)
	geo.merge_polygon_objects(numF, 1)
	cleanMesh(-0.0005,1,1)
	geo.select_objects(1, "Polygon", 1, baseI)
	geo.scale_model(1, 1, 1, 21, 1, 0, 0, 20, 1, 0, 1)
	geo.select_objects(1, "Polygon", 2, baseI, numI)
	geo.merge_polygon_objects(numI, 1)
	cleanMesh(-0.0005,1,1)
#END FUNCTIONS==============================================================================================================================================
#===========================================================================================================================================================
#Execute Import Run ========================================================================================================================================
#===========================================================================================================================================================
def opnMod(path_to_file, each):
	cnumM = [ [None]*5 for rows in range(12)]
	geo.open(0, 1, path_to_file)
	raw1Name = each
	activeModel = geoapp.getActiveModel()
	if activeModel != None:
		geo.select_all()
		geo.clear_all()
		modelName = activeModel.name
		originalMeshIN = geoapp.getMesh( activeModel )
		if originalMeshIN != None:
			#Base Name
			activeModel = geoapp.getActiveModel()
			modelName = activeModel.name
			#Case#, Upper/Lower & Model=============================================
			spnum = modelName.split('-')
			rchk = spnum[1]
			if rchk[0] == 'R':
				caseid = spnum[0] + '-' + spnum[1]
				spnum2 = spnum[2]
			else:
				caseid = spnum[0]
				spnum2 = spnum[1]
			detLFUF = 0
			if spnum2 == "LF": detLFUF = 1
			if spnum2 == "UF": detLFUF = 1
			if detLFUF == 1:
#============================================================================================================================================================
#Model Naming================================================================================================================================================
#============================================================================================================================================================
				cnumM[0][0] = caseid + '-LF'
				cnumM[1][0] = caseid + '-LI'
				cnumM[2][0] = caseid + '-LO'
				cnumM[3][0] = caseid + '-LF-RAW'
				cnumM[4][0] = caseid + '-LI-RAW'
				cnumM[5][0] = caseid + '-UF'
				cnumM[6][0] = caseid + '-UI'
				cnumM[7][0] = caseid + '-UO'
				cnumM[8][0] = caseid + '-UF-RAW'
				cnumM[9][0] = caseid + '-UI-RAW'
				#Occlusion Names======================
				cnumM[10][0] = caseid + '-OCCF'
				cnumM[11][0] = caseid + '-OCCI'
#============================================================================================================================================================
#File Directory=========================================================================================================================================
#============================================================================================================================================================
			#File Origin =================================================================================================================================
				cnumM[0][2] = path_to_watch + cnumM[0][0] + '.wrp'
				cnumM[1][2] = path_to_watch + cnumM[1][0] + '.wrp'
				cnumM[3][2] = Terminal + 'RP_Automation\\RAW\\STLS\\' + cnumM[3][0] + '.stl'
				cnumM[4][2] = Terminal + 'RP_Automation\\RAW\\STLS\\' + cnumM[4][0] + '.stl'
				cnumM[5][2] = path_to_watch + cnumM[5][0] + '.wrp'
				cnumM[6][2] = path_to_watch + cnumM[6][0] + '.wrp'
				cnumM[8][2] = Terminal + 'RP_Automation\\RAW\\STLS\\' + cnumM[8][0] + '.stl'
				cnumM[9][2] = Terminal + 'RP_Automation\\RAW\\STLS\\' + cnumM[9][0] + '.stl'
			#Additional Directory Paths===================================================================================================
				#Save============================
				cnumM[0][3] = savePath + cnumM[0][0] + '.wrp'
				cnumM[1][3] = savePath + cnumM[1][0] + '.wrp'
				cnumM[2][3] = savePath + cnumM[2][0] + '.wrp'
				cnumM[5][3] = savePath + cnumM[5][0] + '.wrp'
				cnumM[6][3] = savePath + cnumM[6][0] + '.wrp'
				cnumM[7][3] = savePath + cnumM[7][0] + '.wrp'
				cnumM[10][3] = savePath + cnumM[10][0] + '.wrp'
				cnumM[11][3] = savePath + cnumM[11][0] + '.wrp'
				#Trash=============================
				cnumM[0][4] = rawPath + cnumM[0][0] + '.wrp'
				cnumM[1][4] = rawPath + cnumM[1][0] + '.wrp'
				cnumM[5][4] = rawPath + cnumM[5][0] + '.wrp'
				cnumM[6][4] = rawPath + cnumM[6][0] + '.wrp'
			#Check File Existence============================================================================================================================================================
				chkffL = 0
				chkffU = 0
				chkffOC = 0
				if not os.path.exists(cnumM[0][2]): chkffL = 1
				if not os.path.exists(cnumM[1][2]): chkffL = 1
				if not os.path.exists(cnumM[3][2]): chkffOC = 1
				if not os.path.exists(cnumM[4][2]): chkffOC = 1
				if not os.path.exists(cnumM[5][2]): chkffU = 1
				if not os.path.exists(cnumM[6][2]): chkffU = 1
				if not os.path.exists(cnumM[8][2]): chkffOC = 1
				if not os.path.exists(cnumM[9][2]): chkffOC = 1
				#============================================================================================================================================
				if chkffL == 1:
					if os.path.exists(cnumM[0][3]):
						if os.path.exists(cnumM[1][3]):
							chkffOC = 0
							cnumM[0][2] = cnumM[0][3]
							cnumM[1][2] = cnumM[1][3]
						else: chkffOC = 1
					else: chkffOC = 1
				if chkffU == 1:
					if os.path.exists(cnumM[5][3]):
						if os.path.exists(cnumM[6][3]):
							chkffOC = 0
							cnumM[5][2] = cnumM[5][3]
							cnumM[6][2] = cnumM[6][3]
						else: chkffOC = 1
					else: chkffOC = 1
#============================================================================================================================================================				
#Lower Processing============================================================================================================================================================
#============================================================================================================================================================				
				if chkffL == 0:
				#Allocate Models/Meshes===================================================================================================================
					#1stPass LF=========================================
					GetFile(cnumM[0][2])
					geo.select_objects(1, "Polygon", 1, cnumM[0][0])
					geo.select_all()
					geo.clear_all()
					geo.exact_position(0, -0.0010, 0, 0, 0, 0, 1, 0, 0, 1)
					cnumM[0][1] = dupObj()
					#1stPass LI==========================================
					GetFile(cnumM[1][2])
					geo.select_objects(1, "Polygon", 1, cnumM[1][0])
					geo.select_all()
					geo.clear_all()
					geo.exact_position(0, -0.0010, 0, 0, 0, 0, 1, 0, 0, 1)
					cnumM[1][1] = dupObj()
				#Process Individual Models===================================================================================================================
					RetObj(cnumM[0][1], cnumM[0][0])
					RetObj(cnumM[1][1], cnumM[1][0])
					baseExt(cnumM[1][0], cnumM[0][0])
					Overlay(cnumM[1][0], cnumM[0][0], cnumM[2][0])
					geo.select_objects(1, "Polygon", 3, cnumM[0][0], cnumM[1][0], cnumM[2][0])
					geo.section_by_plane(1, 0, 1, 1, -0, -1, -0, 0.005, 0)
					geo.section_by_plane(1, 0, 1, 1, -0, -1, -0, 0.002, 0)
					geo.fill_all_holes(1, 0, 1.79e+308, False)
				#Added Volume Check on all parts 11/2/15======================================================================================================
				#Allocate Models======================================================================================================
					geo.select_objects(1, "Polygon", 1, cnumM[0][0])
					volcorrect()
					cnumM[0][1] = dupObj()
					geo.select_objects(1, "Polygon", 1, cnumM[1][0])
					volcorrect()
					cnumM[1][1] = dupObj()
					geo.select_objects(1, "Polygon", 1, cnumM[2][0])
					volcorrect()
					cnumM[2][1] = dupObj()
				#Save Individual Models======================================================================================================
					RetObj(cnumM[0][1], cnumM[0][0])
					geoapp.saveAs(cnumM[0][3])
					cnumM[0][1] = dupObj()
					RetObj(cnumM[1][1], cnumM[1][0])
					geoapp.saveAs(cnumM[1][3])
					cnumM[1][1] = dupObj()
					RetObj(cnumM[2][1], cnumM[2][0])
					geoapp.saveAs(cnumM[2][3])
					cnumM[2][1] = dupObj()
				#Move Input Files======================================================================================================
					shutil.move(cnumM[0][2],cnumM[0][4])
					shutil.move(cnumM[1][2],cnumM[1][4])
#============================================================================================================================================================
#Upper Processing============================================================================================================================================================
#============================================================================================================================================================
				if chkffU == 0:
				#Allocate Models/Meshes===================================================================================================================
					#1stPass UF=========================================
					GetFile(cnumM[5][2])
					geo.select_objects(1, "Polygon", 1, cnumM[5][0])
					geo.select_all()
					geo.clear_all()
					geo.exact_position(0, 0.0010, 0, 0, 0, 180, 1, 0, 0, 1)
					cnumM[5][1] = dupObj()
					#1stPass UI==========================================
					GetFile(cnumM[6][2])
					geo.select_objects(1, "Polygon", 1, cnumM[6][0])
					geo.select_all()
					geo.clear_all()
					geo.exact_position(0, 0.0010, 0, 0, 0, 180, 1, 0, 0, 1)
					cnumM[6][1] = dupObj()
				#Process Individual Models===================================================================================================================
					RetObj(cnumM[5][1], cnumM[5][0])
					RetObj(cnumM[6][1], cnumM[6][0])
					baseExt(cnumM[6][0], cnumM[5][0])
					Overlay(cnumM[6][0], cnumM[5][0], cnumM[7][0])
					geo.select_objects(1, "Polygon", 3, cnumM[5][0], cnumM[6][0], cnumM[7][0])
					geo.section_by_plane(1, 0, 1, 1, -0, -1, -0, 0.005, 0)
					geo.section_by_plane(1, 0, 1, 1, -0, -1, -0, 0.002, 0)
					geo.fill_all_holes(1, 0, 1.79e+308, False)
				#Added Volume Check on all parts 11/2/15======================================================================================================
				#Allocate Models======================================================================================================
					geo.select_objects(1, "Polygon", 1, cnumM[5][0])
					volcorrect()
					cnumM[5][1] = dupObj()
					geo.select_objects(1, "Polygon", 1, cnumM[6][0])
					volcorrect()
					cnumM[6][1] = dupObj()
					geo.select_objects(1, "Polygon", 1, cnumM[7][0])
					volcorrect()
					cnumM[7][1] = dupObj()
				#Save Individual Models======================================================================================================
					RetObj(cnumM[5][1], cnumM[5][0])
					geoapp.saveAs(cnumM[5][3])
					cnumM[5][1] = dupObj()
					RetObj(cnumM[6][1], cnumM[6][0])
					geoapp.saveAs(cnumM[6][3])
					cnumM[6][1] = dupObj()
					RetObj(cnumM[7][1], cnumM[7][0])
					geoapp.saveAs(cnumM[7][3])
					cnumM[7][1] = dupObj()
				#Move Input Files======================================================================================================
					shutil.move(cnumM[5][2],cnumM[5][4])
					shutil.move(cnumM[6][2],cnumM[6][4])
#==========================================================================================================================================================
#Occlusion Processing======================================================================================================================================
#==========================================================================================================================================================
				if chkffOC == 0:
				#Allocate Post Processed if Needed============================================================================================
					if chkffL == 1:
						#Processed LF=========================================
						GetFile(cnumM[0][2])
						geo.select_objects(1, "Polygon", 1, cnumM[0][0])
						cnumM[0][1] = dupObj()
						#Processed LI==========================================
						GetFile(cnumM[1][2])
						geo.select_objects(1, "Polygon", 1, cnumM[1][0])
						cnumM[1][1] = dupObj()
					if chkffU == 1:
						#Processed UF=========================================
						GetFile(cnumM[5][2])
						geo.select_objects(1, "Polygon", 1, cnumM[5][0])
						cnumM[5][1] = dupObj()
						#Processed UI==========================================
						GetFile(cnumM[6][2])
						geo.select_objects(1, "Polygon", 1, cnumM[6][0])
						cnumM[6][1] = dupObj()
				#Allocate Raw Occlusions======================================================================================================
					GetFile(cnumM[3][2])
					geo.select_objects(1, "Polygon", 1, cnumM[3][0])
					cnumM[3][1] = dupObj()
					GetFile(cnumM[4][2])
					geo.select_objects(1, "Polygon", 1, cnumM[4][0])
					cnumM[4][1] = dupObj()
					GetFile(cnumM[8][2])
					geo.select_objects(1, "Polygon", 1, cnumM[8][0])
					cnumM[8][1] = dupObj()
					GetFile(cnumM[9][2])
					geo.select_objects(1, "Polygon", 1, cnumM[9][0])
					cnumM[9][1] = dupObj()
				#Create Occlusions======================================================================================================
					RetObj(cnumM[0][1], cnumM[0][0])
					RetObj(cnumM[3][1], cnumM[3][0])
					RetObj(cnumM[1][1], cnumM[1][0])
					RetObj(cnumM[4][1], cnumM[4][0])
					BFA2(cnumM[3][0], cnumM[0][0], 0)
					BFA2(cnumM[4][0], cnumM[1][0], 0)
					RetObj(cnumM[5][1], cnumM[5][0])
					RetObj(cnumM[8][1], cnumM[8][0])
					RetObj(cnumM[6][1], cnumM[6][0])
					RetObj(cnumM[9][1], cnumM[9][0])
					BFA2(cnumM[8][0], cnumM[5][0], 1)
					BFA2(cnumM[9][0], cnumM[6][0], 1)
					geo.select_objects(1, "Polygon", 1, cnumM[3][0])
					cnumM[3][1] = dupObj()
					geo.select_objects(1, "Polygon", 1, cnumM[4][0])
					cnumM[4][1] = dupObj()
					geo.select_objects(1, "Polygon", 1, cnumM[8][0])
					cnumM[8][1] = dupObj()
					geo.select_objects(1, "Polygon", 1, cnumM[9][0])
					cnumM[9][1] = dupObj()
					#Merge Occlusions=================================
					occ(cnumM[6][0], cnumM[1][0], cnumM[11][0])
					occ(cnumM[5][0], cnumM[0][0], cnumM[10][0])
					BFA2(cnumM[10][0], cnumM[11][0], 2)
				#Save Occlusions======================================================================================================
					geo.select_objects(1, "Polygon", 1, cnumM[11][0])
					cnumM[11][1] = dupObj()
					geo.select_objects(1, "Polygon", 1, cnumM[10][0])
					geoapp.saveAs(cnumM[10][3])
					cnumM[10][1] = dupObj()
					RetObj(cnumM[11][1], cnumM[11][0])
					geoapp.saveAs(cnumM[11][3])
				#============================================================================================================================================================
				#============================================================================================================================================================
#============================================================================================================================================================
#END MACRO AGAINST IMPORT ===================================================================================================================================
#============================================================================================================================================================
		else:
			print( "No Mesh" )
	else:
		print( "Waiting for new case..." )
	geo.new()
#
#File Move=================================================================================
def MoveFile(path_to_file, each):
	shutil.move(path_to_file, os.path.join(savePath, each))
#
def Watch():
	while len(x)==0:
		for each in os.listdir(path_to_watch):
			saveContext()#Initialize Save Point==========================================================================
			if each.endswith("Bdone.txt"):
				dispOn()
				x.append("done")
			else:
				try:
					path_to_file = os.path.join(path_to_watch, each)
					opnMod(path_to_file, each)
					restoreContext()
				except:
					dispOn()
					x.append("done")
#
if __name__=='__main__':
	dispOn()
	dispOff()
	Watch()