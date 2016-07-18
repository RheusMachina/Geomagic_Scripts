import geomagic.app.v2
import time
for m in geomagic.app.v2.execStrings: exec m in locals(), globals()
import os,time,subprocess,shutil,datetime,math,csv

#################################################################################################################################################
#Model Handling
activeModel = geoapp.getActiveModel()
modelName = activeModel.name
originalMesh = geoapp.getMesh( activeModel )
geo.select_objects(0, "Polygon", 1, Index#) 		#Select by Index#
geo.select_objects(0, "Polygon", 2, Index#1, Index#2) 	#Select Multiple by Index#
geo.select_objects(1, "Polygon", 1, Name1) 			#Select by Name
geo.select_objects(1, "Polygon", 2, Name1, Name2) 		#Select Multiple by Name
geo.reorient_model() 						#Reorient Gloabl Coords
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

#################################################################################################################################################
#Active Selection
geo.expand_selection_multi()
geo.shrink_selection_multi()
geo.select_volume(x1, y1, z1, x2, y2, z2)

#################################################################################################################################################
#Mesh Manipulation
geo.mesh_doctor("smallcompsize", 0.0004, "smalltunnelsize", 0.0002, "holesize", 0.0002, "spikesens", 50, "spikelevel", 0.5, "defeatureoption", 2, "fillholeoption", 2, "autoexpand", 2, "operations", "IntersectionCheck+", "SmallComponentCheck+", "SpikeCheck+", "HighCreaseCheck+", "Update", "Auto-Repair")
geo.section_by_plane(xn,yn,zn,xn,yn,zn,x,y,z)
geo.remove_spikes_new(100)
geo.relax_polygons(50, 0, 1, -1, 3)
geo.reduce_noise_poly(2, 4, False, 1.2e-005, 0, False, 5, 1e-005, False, u'')
geo.remesh(0.0003, 1, 0, 180, 0.003, 1, 0, 0, 0.0003, 0)
geo.make_open_manifold()

#################################################################################################################################################
#Geometry Analyzer
#Object X
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
#Object Y
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
#Object Z
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
#Object Volume
def volcheck():
	model = geoapp.getActiveModel()
	mesh = geoapp.getMesh(model)
	analyzer = Analyze(mesh)
	analyzer.run()
	volc = analyzer.volume
	return volc
