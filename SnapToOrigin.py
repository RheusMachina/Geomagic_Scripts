import geomagic.app.v2
import time
for m in geomagic.app.v2.execStrings: exec m in locals(), globals()
import os,time,subprocess,shutil,datetime,math,csv
#
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
dx=xct()
dy=yct()
dz=zct()
geo.move_to_origin(0, dx, dy, dz)