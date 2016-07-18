import geoapiall
for m in geoapiall.modules: exec "from %s import *" % m in locals(), globals()
import geoappall
for m in geoappall.execStrings: exec m in globals(), locals()
import geomagic.app.v2
for m in geomagic.app.v2.execStrings: exec m in locals(), globals()
import os,time,subprocess,shutil,datetime,math

#File Folder Location
Terminal = u'C:\\Users\\Public\\Documents\\MTM Automation\\'
WDP = Terminal + 'RP_Automation\\'

#Working Folders
startPath = WDP + 'A_1st_Review\\'
savePath = WDP + 'B_1stPass_Output\\'
if not os.path.exists(savePath): os.makedirs(savePath)
rawPath = WDP + 'RAW\\STLS\\'
if not os.path.exists(rawPath): os.makedirs(rawPath)
#Declare Functions=============================================================================
#Modified Nomenclature
def ModName(mr):
	activeModel = geoapp.getActiveModel()
	if activeModel != None:
		modelName = activeModel.name
		raw1Name = modelName 
		#Check for Spaces
		spchk = raw1Name.split(' ')
		spa = spchk[0]
		spb = len(spa)-1
		spc = spb + 1
		spy = spa[spb:spc]
		if spy == "l":
			r2n = spchk[1]
			raw2Name = spa + r2n[1:]
		else:
			raw2Name = raw1Name
		#Identify Mandibular/Maxilliary
		#idName = raw2Name.split('_M')
		newName = raw2Name.split('_')
		na= newName[0]
		#Check for Hyphen -r
		hypsplit = na.split('-r')
		hypchk1 = len(na)
		hypchk2 = len(hypsplit[0])
		if hypchk1!=hypchk2:
			na = hypsplit[0] + '-R' + hypsplit[1]
		if newName[1][0:5] == "final":
			nc = "F"
		elif newName[1][0:5] == "Final":
			nc = "F"
		else:
			nc="I"
		if newName[2][0:4] == "Mand":
			nb = "-L"
		elif newName[2][0:4] == "mand":
			nb = "-L"
		else:
			nb = "-U"
		if mr == 0:
			newn = na + nb + nc + '-RAW'
		else:	
			newn = na + nb + nc
			activeModel.name = newn
	return newn
#Save Files====================================================================================
def savf():
	activeModel = geoapp.getActiveModel()
	if activeModel != None:
		num0 = activeModel.name
		num2 = ModName(0)
		num1 = ModName(1)
		geoapp.saveAs(savePath + num1 + u'.wrp')
		shutil.move(os.path.join(startPath, num0 + u'.stl'), os.path.join(rawPath, num2 + u'.stl'))
#Object Duplicate==============================================================================
def dupObj():
	activeModel = geoapp.getActiveModel()
	originalMesh = geoapp.getMesh(activeModel)
	duplicate = Duplicate()
	duplicate.object = originalMesh
	duplicate.run()
	amesh = duplicate.clonedobject
	geoapp.deleteModel( originalMesh )
	return amesh
#Object Add ===================================================================================
def RetObj(fMesh, cnum):
	tempMesh = Mesh()
	merger = MergeMeshes()
	merger.mesh = tempMesh
	merger.meshModelAdd = fMesh
	merger.run()
	tempMesh.name = cnum
	geoapp.addModel( tempMesh, tempMesh.name )
def xct():
	activeModel = geoapp.getActiveModel()
	mesh = geoapp.getMesh(activeModel)
	analyzer = Analyze(mesh)
	analyzer.run()
	cgrav = analyzer.centerOfGravity     
	stra = str(cgrav)
	cgyA = stra.split(",")
	cgxA = cgyA[0].split("(")
	cgx = float(cgxA[1])
	return cgx
def yct():
	activeModel = geoapp.getActiveModel()
	mesh = geoapp.getMesh(activeModel)
	analyzer = Analyze(mesh)
	analyzer.run()
	cgrav = analyzer.centerOfGravity     
	stra = str(cgrav)
	cgyA = stra.split(",")
	cgy = float(cgyA[1])
	return cgy
def zct():
	activeModel = geoapp.getActiveModel()
	mesh = geoapp.getMesh(activeModel)
	analyzer = Analyze(mesh)
	analyzer.run()
	cgrav = analyzer.centerOfGravity     
	stra = str(cgrav)
	cgyA = stra.split(",")
	cgzA = cgyA[2].split(")")
	cgz = float(cgzA[0])
	return cgz
def sphrAdd(x,y,z):
	sphereDiameter = 0.015
	dSphere = CylinderFeature()
	dSphere.initialize(Vector3D(x, -.050, z), Vector3D(x, .050, z), sphereDiameter/2)
	dSphere.axis = Vector3D(0.0, 1.0, 0.0)
	createMeshFrom3DFeature = CreateMeshFrom3DFeature()
	createMeshFrom3DFeature.feature = dSphere
	createMeshFrom3DFeature.maxDeviation=.001
	createMeshFrom3DFeature.run()
	dMesh = createMeshFrom3DFeature.mesh
	return dMesh
def sqrAdd(x,y,z):
	sideLength = 0.015
	plane1 = PlaneFeature()
	plane1.normal = Vector3D(0.0, 0.0, 1.0)
	plane1.origin = Vector3D(x, y, z)
	plane1.uRange = Vector2D(-sideLength,sideLength)
	plane1.vRange = Vector2D(-sideLength/2,sideLength/2)
	createMeshFrom3DFeature = CreateMeshFrom3DFeature()
	createMeshFrom3DFeature.feature = plane1
	createMeshFrom3DFeature.run()
	planeMesh = createMeshFrom3DFeature.mesh
	esel = EdgeSelection(planeMesh)
	esel.markBoundary(True)
	extrude = ExtrudeHeight(planeMesh)
	extrude.height = sideLength*2 
	extrude.direction = Vector3D(0, 0, -1)
	extrude.closeExtrusion = True
	extrude.run(esel.first())
	geoapp.clearActiveTriangleSelection(planeMesh)
	return planeMesh
def ReductCase():
	geo.reorient_model()
	activeModel = geoapp.getActiveModel()
	modelName = activeModel.name
	tempMesh = geoapp.getMesh(activeModel)
	cgx = xct()
	cgy = yct()
	cgz = zct()
	sq1 = sqrAdd(cgx, cgy, cgz)
	sp1 = sphrAdd(cgx, cgy, cgz)
	meshBoolean = BooleanMesh(tempMesh)
	meshBoolean.meshModelAdd = sq1
	meshBoolean.operation = meshBoolean.Subtract1
	meshBoolean.run()
	tempMesh2 = tempMesh
	meshBoolean = BooleanMesh(tempMesh2)
	meshBoolean.meshModelAdd = sp1
	meshBoolean.operation = meshBoolean.Subtract1
	meshBoolean.run()
	geo.reorient_model()
	activeModel = geoapp.getActiveModel()
#Added Selection Expand
	geo.reorient_model()
	cgzA1 = zct()
	cgz = cgzA1*1.05
	geo.select_volume(-0.035, -0.0025, cgz, 0.035, 0.0025, -0.025)
	geo.expand_selection_multi()
	geo.delete_triangles()
	geo.fill_all_holes(2, 0, 1.8e+308, False)
	geo.make_open_manifold()
	geo.reorient_model()
	geo.section_by_plane(1, 0, 1, 1, -0, -1, -0, -0, 0)
	geo.section_by_plane(1, 0, 1, 1, -0, -0, -1, 0, 0)
	geo.reorient_model()
#Added Base Clean
	geo.select_volume(-0.05, -0.001, -0.015, 0.05, 0.001, 0.075)
	geo.remove_spikes_new(100)
	geo.mesh_doctor("smallcompsize", 0.0004, "smalltunnelsize", 0.0002, "holesize", 0.0002, "spikesens", 50, "spikelevel", 0.5, "defeatureoption", 2, "fillholeoption", 2, "autoexpand", 2, "operations", "IntersectionCheck+", "SmallComponentCheck+", "SpikeCheck+", "HighCreaseCheck+", "Update", "Auto-Repair")
	geo.clear_all()
	geo.reorient_model()
#Disable Display===============================================================================
def dispOff():
	print 'DISPLAY OFF'
	geo.set_option("Graphics/Disable Display", 1)
#Enable Display================================================================================
def dispOn():
	print 'DISPLAY ON'
	geo.set_option("Graphics/Disable Display", 0)
#
#Operation 1 Execute==============================================================================
#
dispOff()
geo.select_objects(0, "Polygon", 1, 0)
meshix = [ [None]*2 for volume in range(150)]
i2 = 0
for i in range(1,151):
	activeModel = geoapp.getActiveModel()
	if activeModel != None:
		geo.reorient_model()
		ncx = activeModel.name
		ncxsp = ncx.split('_')
		if ncxsp[0] != 'RP':
			meshix[i2][0] = ncx
			meshix[i2][1] = dupObj()
			i2 += 1
			geo.select_objects(0, "Polygon", 1, 0)
		else:
			termREF = dupObj()
	else:
		geo.select_objects(0, "Polygon", 1, 0)

j2 = 0
for j in range(1,i2+1):
	nj = meshix[j2][0]
	mj = meshix[j2][1]
	RetObj(mj, nj)
	geo.reorient_model()
	ReductCase()
	savf()
	xmesh = dupObj()
	j2 += 1
dispOn()