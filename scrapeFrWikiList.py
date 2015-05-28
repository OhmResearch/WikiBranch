from __future__ import print_function
import urllib2, urllib
from bs4 import BeautifulSoup, Comment
import time
import os



if not os.path.exists('./wiki/liveArticles/fr/'):
	try:
		os.makedirs('./wiki/liveArticles/fr/')
	except:
		pass


def downloadWikiArticle(url):
	link = urllib.unquote(url).decode('utf8').strip()
	#url = 'http://fr.wikipedia.org/'+url


	articleName = link.replace('http://fr.wikipedia.org/wiki/','').strip()
	articleName = articleName.encode('utf-8')
	print(articleName)

	try:
		s = urllib2.urlopen(url).read()
	except:
		pass	

	# in case there is a # (pound) within the link, ignore the # bookmark
	sep = '#'
	articleName = articleName.split(sep, 1)[0]

	try:
		f = open('./wiki/liveArticles/fr/'+articleName+'.html','w')
		print(s,file=f)
		f.close
		time.sleep(0.5)  # to be nice to Wikipedia's servers
	except:
		pass


#with open('lists/ListFrWikiVital.txt','r') as f:  # list of vital articles
with open('lists/listFrenchArticles2Download.txt', 'r') as f:  # list of misc articles
	i=0
	for line in f:
		#i+=1

		#articleName = urllib.unquote(line).decode('utf8').strip()
		#articleName = articleName.replace('http://fr.wikipedia.org/wiki/','').strip()
		#articleName = articleName.encode('utf-8')
		#print('./wiki/liveArticles/'+articleName+'.html')
		#if os.path.isfile('./wiki/liveArticles/fr/'+articleName+'.html'):
		#	print(articleName+' already downloaded')  # in case the script gets interrupted, we don't want to re-download already acquired files
		#else:
		#	print('Article #'+str(i))
		#	downloadWikiArticle(line)


		i+=1

		print('Article #'+str(i))
		articleName = urllib.unquote(line).decode('utf8').strip()
		#articleName = articleName.replace('/wiki/','').strip()
		articleName = articleName.replace('http://fr.wikipedia.org/wiki/','').strip()
		articleName = articleName.encode('utf-8')
		#print('./wiki/liveArticles/'+articleName+'.html')
		# If links have # in the url, remove the # and the subsequent text
		# Thanks http://stackoverflow.com/questions/904746/how-to-remove-all-characters-after-a-specific-character-in-python
		sep = '#'
		articleName = articleName.split(sep, 1)[0]

		if os.path.isfile('./wiki/liveArticles/fr/'+articleName+'.html'):
			print('./wiki/liveArticles/fr/'+articleName+'.html')
			print(articleName+' already downloaded')  # in case the script gets interrupted, we don't want to re-download already acquired files
		else:
			print('./wiki/liveArticles/fr/'+articleName+'.html')
			downloadWikiArticle(line)


