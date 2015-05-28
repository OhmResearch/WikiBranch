from __future__ import print_function
import urllib2, urllib
from bs4 import BeautifulSoup, Comment
import time
import os
from unidecode import unidecode

liveFileDir = '/wiki/liveArticles/'  # dir of your live Wikipedia articles downloaded from scrapeWikiVital.py
staticFileDir = './wiki'  # dir of where you want the static copies of the Wikipedia articles
#mediaFileDir = staticFileDir+'/wiki/en'  # the static articles will be placed within a /wiki/en/ for the English versions

# you'll notice that after we generate a list of media files from the conversion of Wiki pages to static pages, there are tons of duplicates.
# we'd like to regenerate the list so that no duplicates are included
# script should only take about 0.1 seconds to complete

infilename = 'lists/listInfoBoxImgs.txt'
outfilename = 'lists/listInfoBoxImgs-nodup.txt'

lines_seen = set() # holds lines already seen
outfile = open(outfilename, "w")
for line in open(infilename, "r"):
    if line not in lines_seen: # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()


def downloadMedia(line):
	global liveFileDir, staticFileDir, mediaFileDir
	

	mediaFile = urllib.unquote(line).decode('utf8').strip()
	url = 'http:'+mediaFile
	mediaFile = mediaFile.replace('//upload.wikimedia.org/wikipedia','').strip()
	mediaFile = mediaFile.replace('//upload.wikimedia.org','').strip()
	mediaFile = mediaFile.encode('utf-8')
	#print("mediaFile = "+mediaFile)
	url = url.encode('utf-8')

	# Strip restricted FAT characters from the folder and filename strings
	# Without this step, numerous errors arise because certain characters
	# cannot exist on FAT-formatted file systems, such as USB flash drives.
	mediaFile = cleanseMediaFile(mediaFile)


	mediaFileDir = staticFileDir+os.path.dirname(mediaFile)
	
	print('Dirname: '+os.path.dirname(mediaFile))
	print('mediaFile= '+mediaFile)
	#print(mediaFileDir)

	print('URL: '+url)
	print('Save As: '+staticFileDir+mediaFile)
	print('Create Folder: '+mediaFileDir)


	if not os.path.exists(mediaFileDir):
		try:
			os.makedirs(mediaFileDir)
		except:
			pass

	try:
		s = urllib2.urlopen(url).read()
		f = open(staticFileDir+mediaFile,'w')
		print(s,file=f)
		f.close
		print('File Downloaded')
		#time.sleep(0.5)  # to be nice to Wikipedia's servers
	except:
		print('Error retrieving file: '+url)
		print(staticFileDir+mediaFile)
		f = open('lists/getVitalImg-ErrorLog.txt','w')
		print(url,file=f)
		f.close


def cleanseMediaFile(filename):
	filename = urllib.unquote(filename).decode('utf8')
	filename = unidecode(filename)
	#print("filename_in= "+filename)
	#filename = filename.replace('.','')  # .
	#filename = filename.replace('/','')  # /
	#filename = filename.replace("\\",'')  # \

	# Code taken from https://stackoverflow.com/q/1033424
	def remove(value, deletechars):
		for c in deletechars:
			value = value.replace(c,'')
		return value
	
	filename = remove(filename, '#"*;:<>?|+,=[]^~`$@!{}')			# Strip out FAT-restricted characters
	#

	str = filename.split('/')

	filename = ''
	rebuiltFileName = []

	for item in str:
		if (item.__len__() > 255):
			rebuiltFileName.append(item[:250]+item[-5:])    # Needed to keep the last five characters to preserve file extensions
															# in cases of .jpeg
		else:
			rebuiltFileName.append(item)					# Skip string rewrite if string length is already within allowable
															# range of 255 characters								

	filename = '/'.join(rebuiltFileName)

	return filename


with open('lists/listInfoBoxImgs-nodup.txt','r') as f:
	i=0
	for line in f:
		
		i+=1

		print('Media #'+str(i))
		mediaFile = urllib.unquote(line).decode('utf8').strip()
		url = 'http:'+mediaFile
		mediaFile = mediaFile.replace('//upload.wikimedia.org/wikipedia','').strip()
		mediaFile = mediaFile.replace('//upload.wikimedia.org','').strip()
		mediaFile = mediaFile.encode('utf-8')
		url = url.encode('utf-8')
		
		if "#" not in mediaFile:
			print('Check File Exist?: '+staticFileDir+mediaFile)
			if os.path.isfile(staticFileDir+mediaFile):
				print(mediaFile+' already downloaded')  # in case the script gets interrupted, we don't want to re-download already acquired files
			else:
				time.sleep(0.3)
				downloadMedia(line)
				
				
