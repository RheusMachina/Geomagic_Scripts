import geomagic.app.v2
for m in geomagic.app.v2.execStrings: exec m in locals(), globals()
import os,time,subprocess,shutil,datetime 

#Read Triangles#######################
def trnum():
	trgModel = geoapp.getActiveModel() 
	trgMesh = geoapp.getMesh(trgModel)
	tro = float(trgMesh.numTriangles)
	return tro
#Decimate#############################
def dectol(dv):
	if dv != 0:
		tnum = trnum()
		tolm = 1e-005 #Tolerance Value
		geo.decimate_polygons(0, 100, 100, tolm, dv, 0, 0, 3, 0, 3, 2, -1, -1, 3, -tnum)


dectol(1000000)