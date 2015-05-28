from __future__ import print_function
import urllib2, urllib
from bs4 import BeautifulSoup, Comment
import os
import glob
import unicodedata 
import sys
from unidecode import unidecode
import codecs

version = '0.0.10'
debug = True # uncomment for debugging, will force static conversion


# 0.0.10
# Script was failing to correctly name files with special language characters in filename, causing many broken links

# 0.0.9
# Add filename sanitizer for links, e.g., remove restricted characters in links

# 0.0.8
# Math formula images were not showing up because '//upload.wikimedia.org/math/' was not being properly replaced

# 0.0.7
# Added <div id="search-results"> so that search results can display at the top of the page
# Added an Index link in the left navbar

# 0.0.6
# Use unidecode to fix weird folder structure problem
# e(with accent)conomie --> /c/3/, instead of /e/c/

# 0.0.5
# place newly created .html files into /a/b/c.html folder structure

# v0.0.4:
# removes <div> tags with class='bandeau-niveau-detail' with links for more details



reload(sys)  # Reload does the trick!
sys.setdefaultencoding('utf-8')

liveFileDir = './wiki/liveArticles/fr/'  # dir of your live Wikipedia articles downloaded from scrapeWikiVital.py
staticFileDir = './wiki/'  # dir of where you want the static copies of the Wikipedia articles
mediaFileDir = staticFileDir+'fr/'  # the static articles will be placed within a /wiki/en/ for the English versions



if not os.path.exists(mediaFileDir):
		try:
			os.makedirs(mediaFileDir)
		except:
			pass
			

# START 0.0.9 EDIT
def cleansePath(filename):
	filename = unidecode(unicode(filename))
	#print("filename_in= "+filename)
	#Need to clean up or re-write this replace code
	filename = filename.replace('%22','')  # "
	filename = filename.replace('%23','')  # #
	filename = filename.replace('%2A','')  # *
	filename = filename.replace('%3B','')  # ;
	filename = filename.replace('%3A','')  # :
	filename = filename.replace('%3C','')  # <
	filename = filename.replace('%3E','')  # >
	filename = filename.replace('%3F','')  # ?
	filename = filename.replace('%23','')  # |
	filename = filename.replace('%2B','')  # +
	filename = filename.replace('%2C','')  # ,
	filename = filename.replace('%3D','')  # =
	filename = filename.replace('%5B','')  # [
	filename = filename.replace('%5D','')  # ]
	filename = filename.replace('%5E','')  # ^

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
															# in cases of .jpeg/.html
		else:
			rebuiltFileName.append(item)					# Skip string rewrite if string length is already within allowable
															# range of 255 characters								

	filename = '/'.join(rebuiltFileName)
	#print(filename)
	filename = filename.encode('utf-8')
	return filename
# END 0.0.9 EDIT
			

def convertWikiArticle(filename):
	global liveFileDir, staticFileDir, mediaFileDir, version
	englishlink = ''
	imglink = ''

	#articleName = filename
	articleName = cleansePath(filename)
	articleName = urllib.unquote(articleName).decode('utf8').strip()
	articleName = articleName.replace(liveFileDir,'').strip()

	articleName = articleName.encode('utf-8')
	articleName = urllib.unquote_plus(articleName)
	articleTitle = unicode(articleName)
	articleTitle = unidecode(articleTitle)
	articleTitle = str(articleTitle)
	print("ARTICLE NAME LINE 115: "+articleTitle)



	with codecs.open(filename,'r') as f:
		s = f.read()

	

	soup = BeautifulSoup(s)

	searchtag = soup.new_tag('div')
	searchtag.attrs['id'] = 'search-results'
	searchtag.attrs['class'] = 'mw-body'
	searchtag.attrs['style'] = 'display:none;'
	soup.body.insert(1, searchtag)


	searchdiv = soup.find('div', { 'id' : 'search-results'})
	searchtag = soup.new_tag('h1')
	#searchtag.attrs['id'] = 'search-results'
	searchtag.attrs['class'] = 'firstHeading'
	searchtag.string = u'R\u00E9sultats de la recherche'
	searchdiv.insert(1, searchtag)

	searchtag = soup.new_tag('div')
	#searchtag.attrs['id'] = 'search-results'
	searchtag.attrs['class'] = 'mw-body-content'
	searchtag.attrs['style'] = 'margin-top:20px;'
	searchdiv.insert(2, searchtag)

	for div in soup.findAll('html'):
		div['data-version'] = version

	for div in soup.findAll('table', { 'class' : 'navbox' }):
		div.extract()

	for div in soup.findAll('table', { 'class' : 'persondata' }):
		div.extract()

	for div in soup.findAll('div', { 'class' : 'noprint' }):
		div.extract()

	for div in soup.findAll('ul', { 'class' : 'noprint' }):
		div.extract()		

	for div in soup.findAll('noscript'):
		div.extract()		

	for div in soup.findAll('div', { 'class' : 'bandeau-niveau-detail'}):
		div.extract()		



	#for div in soup.findAll('div', { 'class' : 'thumb' }):
	#	div.extract()		

	for div in soup.findAll('div', { 'class' : 'hatnote' }):
		div.extract()		

	for div in soup.findAll('div', { 'class' : 'after-portlet' }):
		div.extract()		

	for div in soup.findAll('div', { 'class' : 'homonymie' }):
		div.extract()		

	for div in soup.findAll('div', { 'id' : 'mw-head' }):
		div.extract()		

	for div in soup.findAll('div', { 'id' : 'p-logo' }):
		div.extract()		

	for div in soup.findAll('div', { 'id' : 'catlinks' }):
		div.extract()		

	for div in soup.findAll('div', { 'id' : 'p-Contribuer' }):
		div.extract()		

	for div in soup.findAll('div', { 'id' : 'p-tb' }):
		div.extract()		

	for div in soup.findAll('div', { 'id' : 'siteNotice' }):
		div.extract()		

	for div in soup.findAll('div', { 'id' : 'jump-to-nav' }):
		div.extract()		

	for div in soup.findAll('div', { 'id' : 'p-coll-print_export' }):
		div.extract()		

	for div in soup.findAll('div', { 'id' : 'section_SpokenWikipedia' }):
		div.extract()		

	for div in soup.findAll('div', { 'class' : 'ns-0' }):
		div.extract()		

	for div in soup.findAll('div', { 'class' : 'topicon' }):
		div.extract()		

	for div in soup.findAll('ul', { 'id' : 'footer-places' }):
		div.extract()		

	for div in soup.findAll('link', { 'rel' : 'dns-prefetch' }):
		div.extract()		

	for div in soup.findAll('link', { 'rel' : 'stylesheet' }):
		div.extract()		

	#for div in soup.findAll('table', { 'class' : 'plainlinks' }):
	#	div.extract()		

	for div in soup.findAll('script'):
		div.extract()		

	for div in soup.findAll('style'):
		div.extract()	

	for div in soup.findAll('span', { 'class' : 'mw-editsection' }):
		div.extract()	

	comments = soup.findAll(text=lambda text:isinstance(text, Comment))
	[comment.extract() for comment in comments]

	styletag = soup.new_tag('link')
	styletag.attrs['rel'] = 'stylesheet'
	styletag.attrs['href'] = '../../../css/style.css'
	soup.head.append(styletag)

	scripttag = soup.new_tag('script')
	scripttag.attrs['src'] = '../../../js/main.js'
	soup.head.append(scripttag)

	for div in soup.findAll('a', { 'class' : 'external text'}):
		div['target'] = '_blank'

	for div in soup.findAll('a', { 'dir' : 'ltr'}):
		#div.unwrap()
		pass

	for div in soup.findAll('a', { 'lang' : 'en' , 'hreflang' : 'en'}):
		englishlink = div['href']
		englishtitle = div['href'].replace('//en.wikipedia.org/wiki/','')
		print('English Link: '+englishlink)  # get the French link for the article to download, and write it to a file to get later
	#	
	#	if frenchlink != '':
	#		with open("lists/listFrenchArticles2Download.txt", "a") as myfile:
	#			myfile.write('http:'+frenchlink+'\n')
	#	else:
	#		with open("lists/missingVitalFrenchArticles.txt", "a") as myfile:
	#			myfile.write(articleName+'\n')

	for div in soup.findAll('li', { 'id' : 'footer-info-copyright'}):
		div.clear()
		div.append(u'Les textes sont disponibles sous ')
		new_tag = soup.new_tag("a", href="../../Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License.html")
		new_tag.string = u'licence Creative Commons paternit\u00E9 partage \u00E0 l\'identique'
		div.append(new_tag)
		div.append(u'; termes droits d\'auteur suppl\u00E9mentaires peuvent s\'appliquer aux images, audio et vid\u00E9o. S\'il vous pla\u00EEt voirt article sur wikipedia.org pour les informations copyright.')

	# Clear and then rebuild the navigation sidebar; needs to be rewritten in reverse order
	for div in soup.findAll('div', { 'id' : 'p-navigation' }):
		div.clear()

		new_tag = soup.new_tag('h3')
		new_tag.string = 'Rechercher Wikipedia'
		div.append(new_tag)
		div.h3['id']='p-navigation-label'


		new_tag = soup.new_tag('input')
		#new_tag.string = 'Search'
		div.append(new_tag)
		div.input['id']='searchInput'
		div.input['type']='search'
		div.input['name']='search'
		div.input['accesskey']='f'
		div.input['placeholder']='Rechercher'
		div.input['style']='margin-left:10px;margin-bottom:10px;width:130px;'


		new_tag = soup.new_tag('h3')
		new_tag.string = 'Navigation'
		div.append(new_tag)
		div.h3['id']='p-navigation-label'

		new_tag = soup.new_tag('div', { 'class' : "body" })
		div.append(new_tag)
		div.div['class']='body'

		new_tag = soup.new_tag('ul')
		div.div.append(new_tag)

		new_tag = soup.new_tag('li')
		div.div.ul.append(new_tag)
		new_tag = soup.new_tag('a')
		new_tag.string = ('Index')
		div.li.append(new_tag)
		div.li.a['href']='../../../en/Article_index.html' 

		new_tag = soup.new_tag('li')
		div.li.insert_before(new_tag)
		new_tag = soup.new_tag('a')
		new_tag.string = u'Math\u00E9matiques'
		div.li.append(new_tag)
		div.li.a['href']=u'../../../fr/Sujet_Math\u00E9matiques.html'  

		new_tag = soup.new_tag('li')
		div.li.insert_before(new_tag)
		new_tag = soup.new_tag('a')
		new_tag.string = u'Technologie'
		div.li.append(new_tag)
		div.li.a['href']=u'../../../fr/Sujet_Technologie.html'  

		new_tag = soup.new_tag('li')
		div.li.insert_before(new_tag)
		new_tag = soup.new_tag('a')
		new_tag.string = u'Sciences physiques'
		div.li.append(new_tag)
		div.li.a['href']=u'../../../fr/Sujet_Sciences_physiques.html'  

		new_tag = soup.new_tag('li')
		div.li.insert_before(new_tag)
		new_tag = soup.new_tag('a')
		new_tag.string = u'Biologie et sciences la sant\u00E9'
		div.li.append(new_tag)
		div.li.a['href']=u'../../../fr/Sujet_Biologie_et_sciences_de_la_sant\u00E9.html'  

		new_tag = soup.new_tag('li')
		div.li.insert_before(new_tag)
		new_tag = soup.new_tag('a')
		new_tag.string = u'Soci\u00E9t\u00E9 et sciences sociales'
		div.li.append(new_tag)
		div.li.a['href']=u'../../../fr/Sujet_Soci\u00E9t\u00E9_et_sciences_sociales.html'  

		new_tag = soup.new_tag('li')
		div.li.insert_before(new_tag)
		new_tag = soup.new_tag('a')
		new_tag.string = u'Vie quotidienne'
		div.li.append(new_tag)
		div.li.a['href']=u'../../../fr/Sujet_Vie_quotidienne.html' 

		new_tag = soup.new_tag('li')
		div.li.insert_before(new_tag)
		new_tag = soup.new_tag('a')
		new_tag.string = u'Philosophie et religion'
		div.li.append(new_tag)
		div.li.a['href']=u'../../../fr/Sujet_Philosophy_and_religion.html'

		new_tag = soup.new_tag('li')
		div.li.insert_before(new_tag)
		new_tag = soup.new_tag('a')
		new_tag.string = u'Arts et culture'
		div.li.append(new_tag)
		div.li.a['href']=u'../../../fr/Sujet_Arts.html'  

		new_tag = soup.new_tag('li')
		div.li.insert_before(new_tag)
		new_tag = soup.new_tag('a')
		new_tag.string = u'G\u00E9ographie'
		div.li.append(new_tag)
		div.li.a['href']=u'../../../fr/Sujet_G\u00E9ographie.html'  

		new_tag = soup.new_tag('li')
		div.li.insert_before(new_tag)
		new_tag = soup.new_tag('a')
		new_tag.string = u'Histoire'
		div.li.append(new_tag)
		div.li.a['href']=u'../../../fr/Sujet_Histoire.html'  

		new_tag = soup.new_tag('li')
		div.li.insert_before(new_tag)
		new_tag = soup.new_tag('a')
		new_tag.string = u'Personnalit\u00E9s'
		div.li.append(new_tag)
		div.li.a['href']=u'../../../fr/Sujet_Personnalit\u00E9s.html'  

		new_tag = soup.new_tag('li')
		div.li.insert_before(new_tag)
		new_tag = soup.new_tag('a')
		new_tag.string = u'Accueil'
		div.li.append(new_tag)
		div.li.a['href']=u'../../../en/Accueil.html'

	# Clear and then rebuild the language sidebar
	for div in soup.findAll('div', { 'id' : 'p-lang' }):
		div.clear()
		new_tag = soup.new_tag('h3')
		new_tag.string = 'Autres langues'
		div.append(new_tag)
		div.h3['id']='p-lang-label'
		new_tag = soup.new_tag('div', { 'class' : "body" })
		div.append(new_tag)
		div.div['class']='body'
		new_tag = soup.new_tag('ul')
		div.div.append(new_tag)



		new_tag = soup.new_tag('li')
		div.div.ul.append(new_tag)


		new_tag = soup.new_tag('a')	
		div.li.append(new_tag)
		div.li.a['href']=articleTitle  # needs to be changed to whatever the French title is
		print("Line 423 articleTitle: "+articleTitle)
		new_tag.string = (u'Fran\u00E7ais')

		new_tag = soup.new_tag('li')
		div.li.insert_before(new_tag)
		if englishlink != '':
			new_tag = soup.new_tag('a')
			new_tag.string = 'English'
			div.li.append(new_tag)
			engArticleTitle = englishlink.replace('//en.wikipedia.org/wiki/','')
			engArticleTitle = urllib.unquote_plus(engArticleTitle)
			articleTitle = unicode(engArticleTitle)
			articleTitle = unidecode(articleTitle)
			print("YO! ARTICLE TITLE = " +articleTitle)
			articleTitle = str(articleTitle)
			articleTitle = articleTitle.translate(None, ",!.;[]\'\":-()*&^%$#@<>?{}=-_+`~")
			articleTitle = articleTitle.lower()
			try:
				articleFolder = articleTitle[0]+'/'+articleTitle[1]+'/'
			except:
				articleFolder = articleTitle[0]+'/'	
			div.li.a['href']='../../../en/'+articleFolder+engArticleTitle+'.html'  # needs to be changed to whatever the French title is
		else:
			new_tag = soup.new_tag('span')
			with open("lists/no-english-for-fr-article.txt", "a") as myfile:
				myfile.write(imglink+'\n')		
	try:			
		for div in soup.find('div', { 'id' : 'mw-content-text' }).findAll('a'):

			hreflink = str(div['href'].encode('utf-8'))
			
			hreflink = cleansePath(hreflink) # 0.0.9 EDIT: remove restricted characters from path
			
			if hreflink[:1] != '#' and '/wiki/' in hreflink:
				#Strip the article title down to only ASCII characters with no symbols
				articleTitleKeep = hreflink.replace('/wiki/','')
				articleTitleKeep = urllib.unquote_plus(articleTitleKeep)
				articleTitleKeep = unicode(articleTitleKeep) #0.0.10 update so that links to filenames have accented/special chars converted to ASCII for FAT storage compatibility
				articleTitleKeep = unidecode(articleTitleKeep)
				articleTitleKeep = str(articleTitleKeep)
				
				articleTitle = unicode(articleTitleKeep)
				articleTitle = unidecode(unicode(articleTitleKeep))
				articleTitle = str(articleTitle)
				articleTitle = articleTitle.translate(None, ",!.;[]\'\":-()*&^%$#@<>?{}=-_+`~")
				articleTitle = articleTitle.lower()
				articleFolder = articleTitle[0]+'/'+articleTitle[1]+'/'
				#print('ArticleFolder: '+articleFolder)
				div['href'] = '../../../fr/'+articleFolder+articleTitleKeep+'.html'
	except:
		print('Couldn\'t find any hyperlinks!')			

	
	try:
		for div in soup.find('div', { 'id' : 'mw-content-text' }).findAll('img'):
			
			imglink = str(div['src'].encode('utf-8'))
			#imglink = imglink.replace('//upload.wikimedia.org/wikipedia/','../')
			#print(imglink)
			if not 'Special:' in imglink:
				print(imglink)
				with open("lists/listInfoBoxImgs-fr.txt", "a") as myfile:
					myfile.write(imglink+'\n')
			div['src'] = unidecode(unicode(cleansePath(imglink).encode('utf-8')))	 	# 0.0.9 EDIT: remove restricted characters from path
			#print(div['src'])										# and limit file path segments to 255 chars

	except:
		pass	

	try:
		for div in soup.find('div', { 'id' : 'mw-content-text' }).findAll('source'):
			
			ogglink = str(div['src'].encode('utf-8'))
			#print(ogglink)
			#ogglink = ogglink.replace('//upload.wikimedia.org/wikipedia/','../')
			#print(imglink)

			with open("lists/listInfoBoxOggs-fr.txt", "a") as myfile:
				myfile.write(ogglink+'\n')

	except:
		pass			


	#soup.prettify()
	

	new_soup = str(soup)
	new_soup = new_soup.replace('//upload.wikimedia.org/wikipedia/','../../../')
	new_soup = new_soup.replace('//upload.wikimedia.org/math/','../../../math/') # 0.0.8 + 0.0.10 (added '/math/')
	
	articleName = articleName.encode('utf-8')
	articleName = urllib.unquote_plus(articleName)
	articleTitle = unicode(articleName)
	articleTitle = unidecode(articleTitle)
	articleTitle = str(articleTitle)
	#articleKeepTitle = str(articleTitle)
	print("ARTICLE TITLE PRE-CONVERT LINE 516: "+articleKeepTitle)

	articleTitle = articleKeepTitle.translate(None, ",!.;[]\'\":-()*&^%$#@<>?{}=-_+`~")
	articleTitle = articleTitle.lower()
	articleFolder = articleTitle[0]+'/'+articleTitle[1]+'/'
	
	print('Checking '+staticFileDir+'fr/'+articleFolder)

	if not os.path.exists(staticFileDir+'fr/'+articleFolder):
		try:
			#print(newFolder+" : "+articleTitle)
			os.makedirs(staticFileDir+'fr/'+articleFolder)
			print('Creating '+staticFileDir+'fr/'+articleFolder)
			#print(articleTitle+' moved to '+newFolder)
		except:
			pass

	try:
		print('Trying to open '+staticFileDir+'fr/'+articleFolder+articleKeepTitle)
		f = open(staticFileDir+'fr/'+articleFolder+articleKeepTitle,'w')
		print(new_soup,file=f)
		f.close
		print('Static save successful!')
	except:
		print('Trying to open '+staticFileDir+'fr/'+articleFolder+articleKeepTitle)
		print('Static save failed!!!')

	return



i=0
for infile in glob.glob( os.path.join('./wiki/liveArticles/fr/', '*.html') ):
	i+=1
	print('Article #'+str(i))
	print(infile)


	articleName = infile
	articleName = urllib.unquote(articleName).decode('utf8').strip()
	articleName = articleName.replace(liveFileDir,'').strip()
	articleName = articleName.encode('utf-8')
	articleName = urllib.unquote_plus(articleName)

	articleTitle = unicode(articleName)
	articleTitle = unidecode(articleTitle)
	articleTitle = str(articleTitle)
	articleKeepTitle = articleTitle
	print("ARTICLE TITLE PRE-CONVERT: "+articleTitle)
	articleTitle = articleTitle.translate(None, ",!.;[]\'\":-()*&^%$#@<>?{}=-_+`~")
	articleTitle = articleTitle.lower()
	articleFolder = articleTitle[0]+'/'+articleTitle[1]+'/'

	try:
		f = open(staticFileDir+'fr/'+articleFolder+articleKeepTitle,'r')
		print('Opening '+staticFileDir+'fr/'+articleFolder+articleKeepTitle+'...')
		for j, line in enumerate(f):
			if j == 1:	
				line = line.strip(' \t\n\r ')
				print(line)			
				if debug == True:
					f.close()
					print('Debug mode. Forcing static conversion.')
					convertWikiArticle(infile)
				elif 'data-version=\"'+version+'\"' in line:

					print('Static version '+version+' already created!')
					f.close()
				else:
					f.close()
					print('Old file version. Converting file now.')
					convertWikiArticle(infile)	
			elif j > 1:
				print('Didn\'t determine version number.')
				break
		


	except:
		if not os.path.isfile(staticFileDir+'fr/'+articleFolder+articleKeepTitle):
			#articleName = articleName.encode('utf-8')
			print(staticFileDir+'fr/'+articleFolder+articleKeepTitle+' doesn\'t exist!')
			print('Converting file now')
			convertWikiArticle(infile)	




