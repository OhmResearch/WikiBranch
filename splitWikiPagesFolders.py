from __future__ import print_function
import urllib2, urllib
from bs4 import BeautifulSoup, Comment
import os, random
import glob
import sys 
import unicodedata 

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('utf-8')

for infile in glob.glob( os.path.join('./wiki/en/', '*.html') ):

	articleTitleKeep = infile.replace('./wiki/en/','')

	#Strip the article title down to only ASCII characters with no symbols
	articleTitle = unicode(articleTitleKeep,'utf-8')
	articleTitle = unicodedata.normalize('NFD', articleTitle).encode('ascii', 'ignore')
	articleTitle = articleTitle.translate(None, ",!.;[]\'\":-()*&^%$#@<>?{}=-_+`~")
	articleTitle = articleTitle.lower()

	#Generate the new folder path where the file will be placed, based on the first and second letters of the file name
	newFolder = './wiki/en/'+articleTitle[0]+'/'+articleTitle[1]+'/'
	


	if not os.path.exists(newFolder):
		try:
			#print(newFolder+" : "+articleTitle)
			os.makedirs(newFolder)
			#print(articleTitle+' moved to '+newFolder)
		except:
			pass

	#Move the file to the proper folder and print success		
	os.rename(infile,newFolder+articleTitleKeep)	
	print(infile+' moved to '+newFolder+articleTitleKeep)	

