# Python script that parses through static Wiki HTML and strips links to pages not within the static collection

from __future__ import print_function
from bs4 import BeautifulSoup, Comment
import os
import glob
import fnmatch

liveFileDir = './wiki/liveArticles/'  # dir of your live Wikipedia articles downloaded from scrapeWikiVital.py
staticFileDir = './wiki/'  # dir of where you want the static copies of the Wikipedia articles
mediaFileDir = staticFileDir+'en/'  # the static articles will be placed within a /wiki/en/ for the English versions


def removeDeadLinks(filename):

	global liveFileDir, staticFileDir, mediaFileDir

	with open(filename,'r') as f:
		s = f.read()

	soup = BeautifulSoup(s)
	soup.prettify()

	try:
		for div in soup.find('div', { 'id' : 'mw-content-text' }).findAll('a'):

			hreflink = str(div['href'].encode('utf-8'))
			#print(hreflink)
			if (hreflink[:1] != '#' and '../' in hreflink) and not ('//' in hreflink[:2]) and not 'redlink=1' in hreflink and not '.php' in hreflink and not 'Subject_' in hreflink:
				#div['href'] = div['href'].replace('/wiki/','../en/')
				#div['href'] += '.html'
				print(hreflink)
				checkfile = hreflink.replace('../../../',staticFileDir)
				print('Checking file... '+checkfile)
				if os.path.isfile(checkfile):
					print('Static: '+hreflink)
				else:
					#div['class']='sever'
					hreflink = 'http://en.wikipedia.org/'+hreflink.replace('../en','wiki')
					#del(div['href'])
					#print(div['class'])

					#UNCOMMENT FOR REALZ
					div.unwrap()

					print('Article not found!')
					#print('Unwraped: '+hreflink)

				#try:
					#print(div['href'])
				#except:
				#	pass
			elif ('redlink=1' in hreflink) or ('//' in hreflink[:2]) or ('Book:' in hreflink) or ('Wikipedia:' in hreflink) or ('Special:' in hreflink) or ('File:' in hreflink) or ('Talk:' in hreflink):
				div.unwrap()	

		soup.prettify()

		try:

			#UNCOMMENT FOR REALZ
			f = open(filename,'w')
			print(soup,file=f)
			f.close

		except:
			pass			
	except:
		print('No hyperlinks found!')

i=0

#matches = []
for root, dirnames, filenames in os.walk(mediaFileDir):
  for filename in fnmatch.filter(filenames, '*.html'):
    if "Subject_" not in filename:
      print(os.path.join(root, filename))
      removeDeadLinks(os.path.join(root, filename))
      

#for infile in glob.glob( os.path.join(mediaFileDir, '*.html') ):
#	#i+=1
#	print('Article #'+str(i))
#	print(infile)
#	removeDeadLinks(infile)
