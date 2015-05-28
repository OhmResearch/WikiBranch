from __future__ import print_function
import urllib2, urllib
from bs4 import BeautifulSoup, Comment
import time
import os

filename = "//upload.wikimedia.org/wikipedia/commons/thumb/8/85/%22Raise_More_Poultry...on_Farms_and_Back_Yards...More_Eggs_and_Poultry_Will_save_Beef_and_Pork.%22_-_NARA_-_512571.tif/lossy-page1-170px-%22Raise_More_Poultry...on_Farms_and_Back_Yards...More_Eggs_and_Poultry_Will_save_Beef_and_Pork.%22_-_NARA_-_512571.tif.jpg"


filename = filename.replace('%2E','')  # .
filename = filename.replace('%2F','')  # /
filename = filename.replace('%5C','')  # \s


filename = urllib.unquote(filename).decode('utf8')

def remove(value, deletechars):
	for c in deletechars:
		value = value.replace(c,'')
	return value
	
filename = remove(filename, '"*;:<>?|+,=[]')			# Strip out FAT-restricted characters


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

print( filename )
