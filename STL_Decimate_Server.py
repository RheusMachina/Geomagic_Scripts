import geomagic.app.v2
for m in geomagic.app.v2.execStrings: exec m in locals(), globals()
import os,time,subprocess,shutil,datetime,math,csv
#
#Target Triangle Count
ttc = 50000 #8175
#
#Define Functions#######################################################################################################################################
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
#
def trnum():
	trgModel = geoapp.getActiveModel() 
	trgMesh = geoapp.getMesh(trgModel)
	tro = float(trgMesh.numTriangles)
	return tro
def dec(dv):
	if dv != 0:
		tnum = trnum()
		tolm = 1e-005 #Tolerance Value
		if tnum > dv: geo.decimate_polygons(0, 100, 100, tolm, dv, 0, 0, 3, 0, 3, 2, -1, -1, 3, -tnum)
########################################################################################################################################################
dx=xct()
dy=yct()
dz=zct()
geo.move_to_origin(0, dx, dy, dz)
#
geo.mesh_doctor("smallcompsize", 0, "smalltunnelsize", 0, "holesize", 0, "spikesens", 50, "spikelevel", 0.5, "defeatureoption", 2, "fillholeoption", 2, "autoexpand", 2, "operations", "IntersectionCheck+", "SmallComponentCheck+", "SpikeCheck+", "HighCreaseCheck+", "Update", "Auto-Repair")
geo.remove_spikes_new(100)
geo.reduce_noise_poly(2, 4, False, 3e-005, 0, False, 5, 5e-005, False, u'')
geo.relax_polygons(50, 0, 1, -1, 0)
geo.remove_spikes_new(100)
#

rmcnt = 0
#
for i in range(0,30):
	tnum = trnum()
	if tnum < 2500000 and tnum > 1750000:
		if rmcnt < 1:
			geo.mesh_doctor("smallcompsize", 0, "smalltunnelsize", 0, "holesize", 0, "spikesens", 50, "spikelevel", 0.5, "defeatureoption", 2, "fillholeoption", 2, "autoexpand", 2, "operations", "SmallComponentCheck+", "Auto-Repair")
			#geo.remesh(1e-005, 1, 0, 45, 0.0002, 1, 0, 0, 1.5e-007, 0)
			#geo.relax_polygons(25, 0, 1, 5e-005, 4)
			geo.remove_spikes_new(100)
			rmcnt += 1
	if tnum < 1000000 and tnum > 750000:
		if rmcnt < 2:
			geo.mesh_doctor("smallcompsize", 0, "smalltunnelsize", 0, "holesize", 0, "spikesens", 50, "spikelevel", 0.5, "defeatureoption", 2, "fillholeoption", 2, "autoexpand", 2, "operations", "SmallComponentCheck+", "Auto-Repair")
			#geo.remesh(2e-005, 1, 0, 45, 0.0002, 1, 0, 0, 7.5e-006, 0)
			#geo.relax_polygons(25, 0, 1, 5e-005, 4)
			geo.remove_spikes_new(100)
			rmcnt += 1
	elif tnum < 170000 and tnum > 120000:
		if rmcnt < 3:
			geo.mesh_doctor("smallcompsize", 0, "smalltunnelsize", 0, "holesize", 0, "spikesens", 50, "spikelevel", 0.5, "defeatureoption", 2, "fillholeoption", 2, "autoexpand", 2, "operations", "SmallComponentCheck+", "Auto-Repair")
			#geo.remesh(4e-005, 1, 0, 45, 0.0002, 1, 0, 0, 1.8e-005, 0)
			#geo.relax_polygons(25, 0, 1, 1e-005, 8)
			rmcnt += 1
	if tnum > ttc:
		#if tnum > 25000:
		if tnum > 71400:
			dval = int(0.7*tnum)
			dec(dval)
		#elif tnum < 25000 and tnum > 11700:
			#dval = 70
			#geo.decimate_polygons(1, dval , dval , 1e-005, 0, 0, 0, 3, 0, 3, 2, -1, -1, 3, -0)
		else:
			dval = (ttc/tnum)*100
			geo.decimate_polygons(1, dval , dval , 1e-005, 0, 0, 0, 3, 0, 3, 2, -1, -1, 3, -0)
#
'''
activeModel = geoapp.getActiveModel() 
snam = activeModel.name
#Template Folder Location
Terminal = u'\\\\C0212-SHARED37\\Phoenix Scans III D\\'
#Terminal = u'E:\\'
pathA = Terminal + u'STL_Brackets\\Raw_Scan_Files\\A_Surfaces_RAW\\' + snam + '.wrp'
pathB = Terminal + u'STL_Brackets\\Raw_Scan_Files\\RAW\\BackUp\\' + snam + '.wrp'
if not os.path.exists(pathA): 
	pathA = Terminal + u'STL_Brackets\\Raw_Scan_Files\\A_Surfaces_RAW\\' + snam + '.stl'
	pathB = Terminal + u'STL_Brackets\\Raw_Scan_Files\\RAW\\BackUp\\' + snam + '.stl'
if os.path.exists(pathA): shutil.move(pathA, pathB)
'''