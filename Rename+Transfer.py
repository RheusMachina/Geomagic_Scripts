import geomagic.app.v2
import time
for m in geomagic.app.v2.execStrings: exec m in locals(), globals()
import os,time,subprocess,shutil,datetime,math,csv

#Template Folder Location
#Terminal = u'\\\\C0212-DICXJ086A\\Phoenix Scans III D\\'
Terminal = u'E:\\'
WDP = Terminal + u'STL_Brackets\\Raw_Scan_Files\\'

#Working Folders
path_to_watch = WDP + 'B_Surfaces_Decimated\\'
savePath = Terminal + u'STL_Brackets\\Finished_STL_Files\\'
path_to_done = WDP + 'RAW\\'


#File Name CSV Reader
fp0 = WDP + 'SKU_List.csv'
fp0_list = list()
with open(fp0,'rb') as f:
	reader = csv.reader(f)
	fp0_list = list(reader)

#
#Watching time intervals
watchtime = 0 #Amount of time between "polling" the folder for new files in seconds
wait4copy = 0 #Amount of time to wait for the file to copy over completely in seconds
x=[] #Empty list to allow user to break out of script running...add a file called "done.txt" to Watch Folder to end script


def opnMod(path_to_file, each):
	geo.open(0, 1, path_to_file)
	activeModel = geoapp.getActiveModel()
	if activeModel != None:
#APPLY MACRO AGAINST IMPORT ==============================================================================
		snam = activeModel.name
		i2 = 0
		for i in range(1, 1901):
			snamlist = fp0_list[i2][0]
			if snamlist == snam: numname = i2
			i2+=1
		print fp0_list[numname][1]
		activeModel = geoapp.getActiveModel()
		activeModel.name = snam + '_' + fp0_list[numname][1]
		snam2 = activeModel.name
		pathA = path_to_watch + snam + '.stl'
		pathB = savePath + fp0_list[numname][2] + '\\'
		if not os.path.exists(pathB): os.makedirs(pathB)
		shutil.move(pathA, pathB + snam2 + '.stl')
#END MACRO AGAINST IMPORT ================================================================================

    
	else:
		print( "No model selected" )
	
	geo.new()

def Watch():
	while len(x)==0:
		time.sleep(watchtime)
		for each in os.listdir(path_to_watch):
			print each
			if each.endswith("z-done.txt") or each.endswith("Document.txt"):
				x.append("done")
			else:
				path_to_file = os.path.join(path_to_watch, each)
				time.sleep(wait4copy)
				opnMod(path_to_file, each)

if __name__=='__main__':
	Watch()