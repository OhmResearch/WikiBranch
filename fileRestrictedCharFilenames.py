import fnmatch
import os
import string
import shutil

for root, dirnames, filenames in os.walk('./wiki/commons/'):
	for filename in fnmatch.filter(filenames, '*\"*.jpeg'):
		oldDir = root
		print(os.path.join(root, filename))
		newDir = string.replace(root,'\"','')
		newDir = string.replace(newDir,'?','')
		newDir = string.replace(newDir,'*','')
		newfilename = string.replace(filename,'\"','')
		newfilename = string.replace(newfilename,'?','')
		newfilename = string.replace(newfilename,'*','')
		print('Renamed to: '+newDir+'/'+newfilename)
		try:
			os.mkdir(newDir)
		except:
		  	pass

		try:  	
			os.rename(os.path.join(root, filename),newDir+'/'+newfilename)
			shutil.rmtree(oldDir+'/')
		except:
			pass

