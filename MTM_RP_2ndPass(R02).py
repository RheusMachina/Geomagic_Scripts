import geomagic.app.v2
import time
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
	cgrav = analyzer.centerOfGravity
	stra = str(cgrav)
	cgyA = stra.split(",")
	cgy = float(cgyA[1])
	return cgy
#Object Z================================================================================
def zloc():
	model = geoapp.getActiveModel()
	mesh = geoapp.getMesh(model)
	analyzer = Analyze(mesh)
	analyzer.run()
	cgrav = analyzer.centerOfGravity
	stra = str(cgrav)
	cgyA = stra.split(",")
	cgzA = cgyA[2].split(")")
	cgz = float(cgzA[0])
	return cgz
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
	if rmd == 1:geo.mesh_doctor("smallcompsize", 0.003, "smalltunnelsize", 0.002, "holesize", 0.002, "spikesens", 50, "spikelevel", 0.5, "defeatureoption", 2, "fillholeoption", 2, "autoexpand", 2, "operations", "IntersectionCheck+", "SmallComponentCheck+", "SpikeCheck+", "HighCreaseCheck+", "Update", "Auto-Repair")
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
	geo.open(0, 1, path_to_file)
	raw1Name = each
	activeModel = geoapp.getActiveModel()
	geo.clear_all()
	if activeModel != None:
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
				cnumLF = caseid + '-LF'
				cnumLI = caseid + '-LI'
				cnumLO = caseid + '-LO'
				rawLF = caseid + '-LF-RAW'
				rawLI = caseid + '-LI-RAW'
				cnumUF = caseid + '-UF'
				cnumUI = caseid + '-UI'
				cnumUO = caseid + '-UO'
				rawUF = caseid + '-UF-RAW'
				rawUI = caseid + '-UI-RAW'
				#Occlusion Names======================
				cnumOCF = caseid + '-OCCF'
				cnumOCI = caseid + '-OCCI'
#============================================================================================================================================================
#File Directory=========================================================================================================================================
#============================================================================================================================================================
			#File Origin =================================================================================================================================
				f1LF = path_to_watch + cnumLF + '.wrp'
				f1LI = path_to_watch + cnumLI + '.wrp'
				frLF = Terminal + 'RP_Automation\\RAW\\STLS\\' + rawLF + '.stl'
				frLI = Terminal + 'RP_Automation\\RAW\\STLS\\' + rawLI + '.stl'
				f1UF = path_to_watch + cnumUF + '.wrp'
				f1UI = path_to_watch + cnumUI + '.wrp'
				frUF = Terminal + 'RP_Automation\\RAW\\STLS\\' + rawUF + '.stl'
				frUI = Terminal + 'RP_Automation\\RAW\\STLS\\' + rawUI + '.stl'
			#Additional Directory Paths===================================================================================================
				#Save============================
				ffuf = savePath + cnumUF + '.wrp'
				ffui = savePath + cnumUI + '.wrp'
				ffuo = savePath + cnumUO + '.wrp'
				fflf = savePath + cnumLF + '.wrp'
				ffli = savePath + cnumLI + '.wrp'
				fflo = savePath + cnumLO + '.wrp'
				ffoci = savePath + cnumOCI + '.wrp'
				ffocf = savePath + cnumOCF + '.wrp'
				#Trash=============================
				ftlf = rawPath + cnumLF + '.wrp'
				ftli = rawPath + cnumLI + '.wrp'
				ftuf = rawPath + cnumUF + '.wrp'
				ftui = rawPath + cnumUI + '.wrp'
			#Check File Existence============================================================================================================================================================
				chkffL = 0
				chkffU = 0
				chkffOC = 0
				if not os.path.exists(f1LF): chkffL = 1
				if not os.path.exists(f1LI): chkffL = 1
				if not os.path.exists(frLF): chkffOC = 1
				if not os.path.exists(frLI): chkffOC = 1
				if not os.path.exists(f1UF): chkffU = 1
				if not os.path.exists(f1UI): chkffU = 1
				if not os.path.exists(frUF): chkffOC = 1
				if not os.path.exists(frUI): chkffOC = 1
				#============================================================================================================================================
				if chkffL == 1:
					if os.path.exists(fflf):
						if os.path.exists(ffli):
							chkffOC = 0
							f1LF = fflf
							f1LI = ffli
						else: chkffOC = 1
					else: chkffOC = 1
				if chkffU == 1:
					if os.path.exists(ffuf):
						if os.path.exists(ffui):
							chkffOC = 0
							f1UF = ffuf
							f1UI = ffui
						else: chkffOC = 1
					else: chkffOC = 1
#============================================================================================================================================================				
#Lower Processing============================================================================================================================================================
#============================================================================================================================================================				
				if chkffL == 0:
				#Allocate Models/Meshes===================================================================================================================
					LImesh = Mesh()
					LFmesh = Mesh()
					LOmesh = Mesh()
					#1stPass LF=========================================
					GetFile(f1LF)
					geo.select_objects(1, "Polygon", 1, cnumLF)
					geo.select_all()
					geo.clear_all()
					geo.exact_position(0, -0.0010, 0, 0, 0, 0, 1, 0, 0, 1)
					LFmesh = dupObj()
					#1stPass LI==========================================
					GetFile(f1LI)
					geo.select_objects(1, "Polygon", 1, cnumLI)
					geo.select_all()
					geo.clear_all()
					geo.exact_position(0, -0.0010, 0, 0, 0, 0, 1, 0, 0, 1)
					LImesh = dupObj()
				#Process Individual Models===================================================================================================================
					RetObj(LFmesh, cnumLF)
					RetObj(LImesh, cnumLI)
					baseExt(cnumLI, cnumLF)
					Overlay(cnumLI, cnumLF, cnumLO)
					geo.select_objects(1, "Polygon", 3, cnumLF, cnumLI, cnumLO)
					geo.section_by_plane(1, 0, 1, 1, -0, -1, -0, 0.005, 0)
					geo.section_by_plane(1, 0, 1, 1, -0, -1, -0, 0.002, 0)
					geo.fill_all_holes(1, 0, 1.79e+308, False)
				#Added Volume Check on all parts 11/2/15======================================================================================================
				#Allocate Models======================================================================================================
					geo.select_objects(1, "Polygon", 1, cnumLF)
					volcorrect()
					LFmesh = dupObj()
					geo.select_objects(1, "Polygon", 1, cnumLI)
					volcorrect()
					LImesh = dupObj()
					geo.select_objects(1, "Polygon", 1, cnumLO)
					volcorrect()
					LOmesh = dupObj()
				#Save Individual Models======================================================================================================
					RetObj(LFmesh, cnumLF)
					geoapp.saveAs(fflf)
					LFmesh = dupObj()
					RetObj(LImesh, cnumLI)
					geoapp.saveAs(ffli)
					LImesh = dupObj()
					RetObj(LOmesh, cnumLO)
					geoapp.saveAs(fflo)
					LOmesh = dupObj()
				#Move Input Files======================================================================================================
					shutil.move(f1LF,ftlf)
					shutil.move(f1LI,ftli)
#============================================================================================================================================================
#Upper Processing============================================================================================================================================================
#============================================================================================================================================================
				if chkffU == 0:
				#Allocate Models/Meshes===================================================================================================================
					UImesh = Mesh()
					UFmesh = Mesh()
					UOmesh = Mesh()
					#1stPass UF=========================================
					GetFile(f1UF)
					geo.select_objects(1, "Polygon", 1, cnumUF)
					geo.select_all()
					geo.clear_all()
					geo.exact_position(0, 0.0010, 0, 0, 0, 180, 1, 0, 0, 1)
					UFmesh = dupObj()
					#1stPass UI==========================================
					GetFile(f1UI)
					geo.select_objects(1, "Polygon", 1, cnumUI)
					geo.select_all()
					geo.clear_all()
					geo.exact_position(0, 0.0010, 0, 0, 0, 180, 1, 0, 0, 1)
					UImesh = dupObj()
				#Process Individual Models===================================================================================================================
					RetObj(UFmesh, cnumUF)
					RetObj(UImesh, cnumUI)
					baseExt(cnumUI, cnumUF)
					Overlay(cnumUI, cnumUF, cnumUO)
					geo.select_objects(1, "Polygon", 3, cnumUF, cnumUI, cnumUO)
					geo.section_by_plane(1, 0, 1, 1, -0, -1, -0, 0.005, 0)
					geo.section_by_plane(1, 0, 1, 1, -0, -1, -0, 0.002, 0)
					geo.fill_all_holes(1, 0, 1.79e+308, False)
				#Added Volume Check on all parts 11/2/15======================================================================================================
				#Allocate Models======================================================================================================
					geo.select_objects(1, "Polygon", 1, cnumUF)
					volcorrect()
					UFmesh = dupObj()
					geo.select_objects(1, "Polygon", 1, cnumUI)
					volcorrect()
					UImesh = dupObj()
					geo.select_objects(1, "Polygon", 1, cnumUO)
					volcorrect()
					UOmesh = dupObj()
				#Save Individual Models======================================================================================================
					RetObj(UFmesh, cnumUF)
					geoapp.saveAs(ffuf)
					UFmesh = dupObj()
					RetObj(UImesh, cnumUI)
					geoapp.saveAs(ffui)
					UImesh = dupObj()
					RetObj(UOmesh, cnumUO)
					geoapp.saveAs(ffuo)
					UOmesh = dupObj()
				#Move Input Files======================================================================================================
					shutil.move(f1UF,ftuf)
					shutil.move(f1UI,ftui)
#==========================================================================================================================================================
#Occlusion Processing======================================================================================================================================
#==========================================================================================================================================================
				if chkffOC == 0:
				#Allocate Post Processed if Needed============================================================================================
					if chkffL == 1:
						LFmesh = Mesh()
						LImesh = Mesh()
						#Processed LF=========================================
						GetFile(f1LF)
						geo.select_objects(1, "Polygon", 1, cnumLF)
						LFmesh = dupObj()
						#Processed LI==========================================
						GetFile(f1LI)
						geo.select_objects(1, "Polygon", 1, cnumLI)
						LImesh = dupObj()
					if chkffU == 1:
						UFmesh = Mesh()
						UImesh = Mesh()
						#Processed UF=========================================
						GetFile(f1UF)
						geo.select_objects(1, "Polygon", 1, cnumUF)
						UFmesh = dupObj()
						#Processed UI==========================================
						GetFile(f1UI)
						geo.select_objects(1, "Polygon", 1, cnumUI)
						UImesh = dupObj()
				#Allocate Raw Occlusions======================================================================================================
					OCImesh = Mesh()
					OCFmesh = Mesh()
					rawLImesh = Mesh()
					rawLFmesh = Mesh()
					rawUImesh = Mesh()
					rawUFmesh = Mesh()
					GetFile(frLF)
					geo.select_objects(1, "Polygon", 1, rawLF)
					rawLFmesh = dupObj()
					GetFile(frLI)
					geo.select_objects(1, "Polygon", 1, rawLI)
					rawLImesh = dupObj()
					GetFile(frUF)
					geo.select_objects(1, "Polygon", 1, rawUF)
					rawUFmesh = dupObj()
					GetFile(frUI)
					geo.select_objects(1, "Polygon", 1, rawUI)
					rawUImesh = dupObj()
				#Create Occlusions======================================================================================================
					RetObj(LFmesh, cnumLF)
					RetObj(rawLFmesh, rawLF)
					RetObj(LImesh, cnumLI)
					RetObj(rawLImesh, rawLI)
					BFA2(rawLF, cnumLF, 0)
					BFA2(rawLI, cnumLI, 0)
					RetObj(UFmesh, cnumUF)
					RetObj(rawUFmesh, rawUF)
					RetObj(UImesh, cnumUI)
					RetObj(rawUImesh, rawUI)
					BFA2(rawUF, cnumUF, 1)
					BFA2(rawUI, cnumUI, 1)
					geo.select_objects(1, "Polygon", 1, rawLF)
					rawLFmesh = dupObj()
					geo.select_objects(1, "Polygon", 1, rawLI)
					rawLImesh = dupObj()
					geo.select_objects(1, "Polygon", 1, rawUF)
					rawUFmesh = dupObj()
					geo.select_objects(1, "Polygon", 1, rawUI)
					rawUImesh = dupObj()
					#Merge Occlusions=================================
					occ(cnumUI, cnumLI, cnumOCI)
					occ(cnumUF, cnumLF, cnumOCF)
					BFA2(cnumOCF, cnumOCI, 2)
				#Save Occlusions======================================================================================================
					geo.select_objects(1, "Polygon", 1, cnumOCI)
					OCImesh = dupObj()
					geo.select_objects(1, "Polygon", 1, cnumOCF)
					geoapp.saveAs(ffocf)
					OCFmesh = dupObj()
					RetObj(OCImesh, cnumOCI)
					geoapp.saveAs(ffoci)
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