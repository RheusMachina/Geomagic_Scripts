import geomagic.app.v2
import time
for m in geomagic.app.v2.execStrings: exec m in locals(), globals()
import os,time,subprocess, shutil, datetime 
import math
import csv
import os


#File Folder Location
WDP = u'C:\\Users\\distt266\\Desktop\\OrthoLab\\Bases\\'

#Working Folders
path_to_watch = WDP + 'ALL\\'
savePath = WDP + 'SAVE\\'
path_to_done = WDP + 'RAW\\'

#
#Watching time intervals
watchtime = 0 #Amount of time between "polling" the folder for new files in seconds
wait4copy = 0 #Amount of time to wait for the file to copy over completely in seconds
x=[] #Empty list to allow user to break out of script running...add a file called "done.txt" to Watch Folder to end script


def opnMod(path_to_file, each):
	geo.open(0, 1, path_to_file)
	# Get the currently selected model in the model manager.
	activeModel = geoapp.getActiveModel()
	
	# Make sure there is a model selected.
	if activeModel != None:
		
		modelName = activeModel.name
		originalMesh = geoapp.getMesh( activeModel )

		# Make sure there is a mesh
		if originalMesh != None:

#APPLY MACRO AGAINST IMPORT ==============================================================================


			geo.to_polygons()


#END MACRO AGAINST IMPORT ================================================================================


			print "Saving", str( savePath + modelName + u'.wrp' )
			geoapp.saveAs( savePath + modelName + u'.wrp' )
			geoapp.deleteModel( originalMesh )

		else:
			print( "This model does not contain a mesh" )
    
	else:
		print( "No model selected" )
	
	geo.new()
	MoveFile(path_to_file, each)

		
def MoveFile(path_to_file, each):
	timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
	shutil.move(path_to_file, os.path.join(path_to_done, str(timestamp) + "_" + each))
	print "Moving file from %s" % path_to_file
	print "Moving file to %s" % os.path.join(path_to_done,each)
	print "Waiting for next case..."


def Watch():
	while len(x)==0:
		time.sleep(watchtime)
		for each in os.listdir(path_to_watch):
			print each
			if each.endswith("done.txt") or each.endswith("Document.txt"):
				x.append("done")
			else:
				path_to_file = os.path.join(path_to_watch, each)
				time.sleep(wait4copy)
				opnMod(path_to_file, each)

if __name__=='__main__':
	Watch()