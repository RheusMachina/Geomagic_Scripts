import geoapiall
for m in geoapiall.modules: exec "from %s import *" % m in locals(), globals()
import geoappall
for m in geoappall.execStrings: exec m in globals(), locals()
import geomagic.app.v2
for m in geomagic.app.v2.execStrings: exec m in locals(), globals()
import os,time,subprocess,shutil,datetime,math
#
#File Folder Location
Terminal = u'C:\\Users\\Public\\Documents\\MTM Automation\\'
WDP = Terminal + 'RP_Automation\\'
#
#Working Folders
startPath = WDP + 'B_1stPass_Output\\'
savePath = WDP + 'B_2ndPass_Input\\'
if not os.path.exists(savePath): os.makedirs(savePath)
rawPath = WDP + 'RAW\\'
if not os.path.exists(rawPath): os.makedirs(rawPath)
#File Save========================================================================================
def savf():
	activeModel = geoapp.getActiveModel()
	if activeModel != None:
		num1 = activeModel.name
		geoapp.saveAs(savePath + num1 + u'.wrp')
		shutil.move(os.path.join(startPath, num1 + u'.wrp'), os.path.join(rawPath, num1 + u'.wrp'))
#Object Duplicate=================================================================================
def dupObj():
	activeModel = geoapp.getActiveModel()
	originalMesh = geoapp.getMesh(activeModel)
	duplicate = Duplicate()
	duplicate.object = originalMesh
	duplicate.run()
	amesh = duplicate.clonedobject
	geoapp.deleteModel( originalMesh )
	return amesh
#Object Add ======================================================================================
def RetObj(fMesh, cnum):
	tempMesh = Mesh()
	merger = MergeMeshes()
	merger.mesh = tempMesh
	merger.meshModelAdd = fMesh
	merger.run()
	tempMesh.name = cnum
	geoapp.addModel( tempMesh, tempMesh.name )
#Disable Display==================================================================================
def dispOff():
	print 'DISPLAY OFF'
	geo.set_option("Graphics/Disable Display", 1)
#Enable Display===================================================================================
def dispOn():
	print 'DISPLAY ON'
	geo.set_option("Graphics/Disable Display", 0)
#
#Operation 2 Execute==============================================================================
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
#
j2 = 0
for j in range(1,i2+1):
	nj = meshix[j2][0]
	mj = meshix[j2][1]
	RetObj(mj, nj)
	savf()
	xmesh = dupObj()
	j2 += 1
dispOn()