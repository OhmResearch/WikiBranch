from __future__ import print_function
import urllib2, urllib
from bs4 import BeautifulSoup, Comment
import os, random
import glob
import unicodedata 
import sys
from unidecode import unidecode

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('utf-8')

liveFileDir = './wiki/liveArticles/'  # dir of your live Wikipedia articles downloaded from scrapeWikiVital.py
staticFileDir = './wiki/'  # dir of where you want the static copies of the Wikipedia articles
mediaFileDir = staticFileDir+'en/'  # the static articles will be placed within a /wiki/en/ for the English versions

version = '0.0.10'
#debug = True # uncomment for debugging, will force static conversion


# 0.0.10
# Script was failing to correctly name files with special language characters in filename, causing many broken links

# 0.0.4
# Fixed a code error where the French language link was href'ing to /fr/[English article title].html
# Fixed code error for English language link was href'ing to /en/[article].html.html

# 0.0.6
# Fixed a unicode decoding error, where unicode characters were not being decomposed correctly. Fixed with unidecode module
# Added <div id="search-results"> so that search result scan display at the top of the page
# Added an Index link in the left navbar

# 0.0.7
# Corrected another unidecode error, didn't fix it in each instance of 0.0.6

# 0.0.8
# Math formula images were not showing up because '//upload.wikimedia.org/math/' was not being properly replaced

# 0.0.9
# Add filename sanitizer for links, e.g., remove restricted characters in links

if not os.path.exists(mediaFileDir):
		try:
			os.makedirs(mediaFileDir)
		except:
			pass

# START 0.0.9 EDIT
def cleansePath(filename):
	filename = unidecode(filename)
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
	print(filename)
	filename = filename.encode('utf-8')
	return filename
# END 0.0.9 EDIT

def convertWikiArticle(filename):
	global liveFileDir, staticFileDir, mediaFileDir
	frenchlink = ''

	with open(filename,'r') as f:
		s = f.read()

	articleName = cleansePath(filename)
	articleName = urllib.unquote(articleName).decode('utf8').strip()
	articleName = articleName.replace(liveFileDir,'').strip()
	#print(articleName)

	soup = BeautifulSoup(s)

	searchtag = soup.new_tag('div')
	searchtag.attrs['id'] = 'search-results'
	searchtag.attrs['class'] = 'mw-body'
	searchtag.attrs['style'] = 'display:none;'
	try:
		soup.body.insert(1, searchtag)
	except:
		pass	


	searchdiv = soup.find('div', { 'id' : 'search-results'})
	searchtag = soup.new_tag('h1')
	#searchtag.attrs['id'] = 'search-results'
	searchtag.attrs['class'] = 'firstHeading'
	searchtag.string = u'Search results'
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

	#for div in soup.findAll('div', { 'class' : 'thumb' }):
	#	div.extract()		

	for div in soup.findAll('div', { 'class' : 'hatnote' }):
		div.extract()		

	for div in soup.findAll('div', { 'class' : 'after-portlet' }):
		div.extract()		

	for div in soup.findAll('div', { 'id' : 'mw-head' }):
		div.extract()		

	for div in soup.findAll('div', { 'id' : 'p-logo' }):
		div.extract()		

	for div in soup.findAll('div', { 'id' : 'catlinks' }):
		div.extract()		

	for div in soup.findAll('div', { 'id' : 'p-interaction' }):
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

	try:
		for div in soup.findAll('a', { 'lang' : 'fr' , 'hreflang' : 'fr'}):
			frenchlink = div['href']
			#print('FrenchLink: '+frenchlink)  # get the French link for the article to download, and write it to a file to get later
			
			if frenchlink != '':
				# If there is a French article available, add it to a file for future download
				with open("lists/listFrenchArticles2Download.txt", "a") as myfile: 
					myfile.write('http:'+frenchlink+'\n')
	except:
		# If there is no French article available, then add title to a file for future reference
		with open("lists/missingVitalFrenchArticles.txt", "a") as myfile:
			myfile.write(articleName+'\n')

	for div in soup.findAll('li', { 'id' : 'footer-info-copyright'}):
		div.clear()
		div.append('Text is available under the ')
		new_tag = soup.new_tag("a", href="../../Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License.html")
		new_tag.string = 'Creative Commons Attribution-ShareAlike License'
		div.append(new_tag)
		div.append('; additional copyright terms may apply to images, audio and video.  Please see this article on wikipedia.org for copyright information.')

	# Clear and then rebuild the navigation sidebar; needs to be rewritten in reverse order
	for div in soup.findAll('div', { 'id' : 'p-navigation' }):
		div.clear()

		new_tag = soup.new_tag('h3')
		new_tag.string = 'Search Wikipedia'
		div.append(new_tag)
		div.h3['id']='p-navigation-label'


		new_tag = soup.new_tag('input')
		#new_tag.string = 'Search'
		div.append(new_tag)
		div.input['id']='searchInput'
		div.input['type']='search'
		div.input['name']='search'
		div.input['accesskey']='f'
		div.input['placeholder']='Search'
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
		new_tag.string = ('Mathematics')
		div.li.append(new_tag)
		div.li.a['href']='../../../en/Subject_Mathematics.html'  

		new_tag = soup.new_tag('li')
		div.li.insert_before(new_tag)
		new_tag = soup.new_tag('a')
		new_tag.string = ('Technology')
		div.li.append(new_tag)
		div.li.a['href']='../../../en/Subject_Technology.html'  

		new_tag = soup.new_tag('li')
		div.li.insert_before(new_tag)
		new_tag = soup.new_tag('a')
		new_tag.string = ('Physical sciences')
		div.li.append(new_tag)
		div.li.a['href']='../../../en/Subject_Physical_sciences.html'  

		new_tag = soup.new_tag('li')
		div.li.insert_before(new_tag)
		new_tag = soup.new_tag('a')
		new_tag.string = ('Biology and health sciences')
		div.li.append(new_tag)
		div.li.a['href']='../../../en/Subject_Biology_and_health_sciences.html'  

		new_tag = soup.new_tag('li')
		div.li.insert_before(new_tag)
		new_tag = soup.new_tag('a')
		new_tag.string = ('Society and social sciences')
		div.li.append(new_tag)
		div.li.a['href']='../../../en/Subject_Society_and_social_sciences.html'  

		new_tag = soup.new_tag('li')
		div.li.insert_before(new_tag)
		new_tag = soup.new_tag('a')
		new_tag.string = ('Everyday life')
		div.li.append(new_tag)
		div.li.a['href']='../../../en/Subject_Everyday_life.html' 

		new_tag = soup.new_tag('li')
		div.li.insert_before(new_tag)
		new_tag = soup.new_tag('a')
		new_tag.string = ('Philosophy and religion')
		div.li.append(new_tag)
		div.li.a['href']='../../../en/Subject_Philosophy_and_religion.html'

		new_tag = soup.new_tag('li')
		div.li.insert_before(new_tag)
		new_tag = soup.new_tag('a')
		new_tag.string = ('Arts')
		div.li.append(new_tag)
		div.li.a['href']='../../../en/Subject_Arts.html'  

		new_tag = soup.new_tag('li')
		div.li.insert_before(new_tag)
		new_tag = soup.new_tag('a')
		new_tag.string = ('Geography')
		div.li.append(new_tag)
		div.li.a['href']='../../../en/Subject_Geography.html'  

		new_tag = soup.new_tag('li')
		div.li.insert_before(new_tag)
		new_tag = soup.new_tag('a')
		new_tag.string = ('History')
		div.li.append(new_tag)
		div.li.a['href']='../../../en/Subject_History.html'  

		new_tag = soup.new_tag('li')
		div.li.insert_before(new_tag)
		new_tag = soup.new_tag('a')
		new_tag.string = ('People')
		div.li.append(new_tag)
		div.li.a['href']='../../../en/Subject_People.html'  

		new_tag = soup.new_tag('li')
		div.li.insert_before(new_tag)
		new_tag = soup.new_tag('a')
		new_tag.string = 'Main Page'
		div.li.append(new_tag)
		div.li.a['href']='../../../en/Main_Page.html'

	# Clear and then rebuild the language sidebar
	for div in soup.findAll('div', { 'id' : 'p-lang' }):
		div.clear()
		new_tag = soup.new_tag('h3')
		new_tag.string = 'Languages'
		div.append(new_tag)
		div.h3['id']='p-lang-label'
		new_tag = soup.new_tag('div', { 'class' : "body" })
		div.append(new_tag)
		div.div['class']='body'
		new_tag = soup.new_tag('ul')
		div.div.append(new_tag)



		new_tag = soup.new_tag('li')
		div.div.ul.append(new_tag)

		try:
			print("Finding frenchlink")
			if frenchlink != '':
				new_tag = soup.new_tag('a')	
				div.li.append(new_tag)
				frenchArticleTitle = frenchlink.replace('//fr.wikipedia.org/wiki/','')
				frenchArticleTitle = urllib.unquote_plus(frenchArticleTitle)
				frenchArticleTitle = unidecode(unicode(frenchArticleTitle)) #0.0.10 French article title was not decoded correctly
				print(frenchArticleTitle+' is the French article title')
				articleTitle = unicode(frenchArticleTitle)
				articleTitle = unidecode(articleTitle)
				articleTitle = str(articleTitle)
				articleTitle = articleTitle.translate(None, ",!.;[]\'\":-()*&^%$#@<>?{}=-_+`~")
				articleTitle = articleTitle.lower()
				
				try:
					articleFolder = articleTitle[0]+'/'+articleTitle[1]+'/'
				except:
					articleFolder = articleTitle[0]+'/'
					
				div.li.a['href']='../../../fr/'+articleFolder+frenchArticleTitle+'.html'  # needs to be changed to whatever the French title is
				print('../../../fr/'+articleFolder+frenchArticleTitle+'.html')
				new_tag.string = (u'Fran\u00E7ais')
				#print(div.li.a['href'])
			else:
				new_tag = soup.new_tag('span')
		except:
			pass		



		new_tag = soup.new_tag('li')
		div.li.insert_before(new_tag)
		new_tag = soup.new_tag('a')
		new_tag.string = 'English'
		div.li.append(new_tag)
		div.li.a['href']=articleName
		
	try:
		for div in soup.find('div', { 'id' : 'mw-content-text' }).findAll('a'):

			hreflink = str(div['href'].encode('utf-8'))
			
			hreflink = cleansePath(hreflink) # 0.0.9 EDIT: remove restricted characters from path
			
			if hreflink[:1] != '#' and '/wiki/' in hreflink and not ':' in hreflink and not '.org' in hreflink:
				#Strip the article title down to only ASCII characters with no symbols
				
				articleTitleKeep = hreflink.replace('/wiki/','')
				articleTitleKeep = urllib.unquote_plus(articleTitleKeep)
				articleTitleKeep = unicode(articleTitleKeep) #0.0.10 update so that links to other pages have accented/special chars converted to ASCII for FAT storage compatibility
				articleTitleKeep = unidecode(articleTitleKeep)
				articleTitleKeep = str(articleTitleKeep)
				
				articleTitle = unicode(articleTitleKeep)
				articleTitle = unidecode(articleTitleKeep)
				articleTitle = str(articleTitle)
				articleTitle = articleTitle.translate(None, ",!.;[]\'\":-()*&^%$#@<>?{}=-_+`~")
				articleTitle = articleTitle.lower()
				articleFolder = articleTitle[0]+'/'+articleTitle[1]+'/'
				div['href'] = '../../../en/'+articleFolder+articleTitleKeep+'.html'
				#print(div['href'])
	except:
		pass			

	
	try:
		for div in soup.find('div', { 'id' : 'mw-content-text' }).findAll('img'):
			
			imglink = str(div['src'].encode('utf-8'))
		
			#imglink = imglink.replace('//upload.wikimedia.org/wikipedia/','../') 
			# I THINK THIS NEEDS TO BE CHANGED SO THAT THE SRC LINK IS CORRECT # 0.0.8
			# STILL HAVE LINKS WITH WIKIMEDIA.ORG IN THEM # 0.0.8
			# like Longitude.html # 0.0.8
			# EDIT 2 # 0.0.8
			# i think i corrected this problem by adding the line: # 0.0.8
			# new_soup = new_soup.replace('//upload.wikimedia.org/math/','../../../') below # 0.0.8

			#print('imglink: '+imglink)
			if not 'Special:' in imglink:
				#print(imglink)
				with open("lists/listInfoBoxImgs.txt", "a") as myfile:
					myfile.write(imglink+'\n')

			div['src'] = unidecode(cleansePath(imglink).encode('utf-8'))	 	# 0.0.9 EDIT: remove restricted characters from path
			#print(div['src'])										# and limit file path segments to 255 chars


	except:
		pass	

	try:
		for div in soup.find('div', { 'id' : 'mw-content-text' }).findAll('source'):
			
			ogglink = str(div['src'].encode('utf-8'))
			#sprint(ogglink)
			#ogglink = ogglink.replace('//upload.wikimedia.org/wikipedia/','../')
			#print(imglink)

			with open("lists/listInfoBoxOggs.txt", "a") as myfile:
				myfile.write(ogglink+'\n')

	except:
		pass			


	


	soup.prettify()
	

	new_soup = str(soup)
	new_soup = new_soup.replace('//upload.wikimedia.org/wikipedia/','../../../')
	new_soup = new_soup.replace('//upload.wikimedia.org/math/','../../../math/') # 0.0.8 + 0.0.10 (added '/math/')
	
	articleName = articleName.encode('utf-8')
	articleName = urllib.unquote_plus(articleName)
	articleTitle = unicode(articleName)
	articleTitle = unidecode(articleTitle)
	articleTitle = str(articleTitle)

	articleTitle = articleTitle.translate(None, ",!.;[]\'\":-()*&^%$#@<>?{}=-_+`~")
	articleTitle = articleTitle.lower()
	articleFolder = articleTitle[0]+'/'+articleTitle[1]+'/'
	
	print('Checking '+staticFileDir+'en/'+articleFolder)

	if not os.path.exists(staticFileDir+'en/'+articleFolder):
		try:
			#print(newFolder+" : "+articleTitle)
			os.makedirs(staticFileDir+'en/'+articleFolder)
			print('Creating '+staticFileDir+'en/'+articleFolder)
			#print(articleTitle+' moved to '+newFolder)
		except:
			pass

	try:
		print('Trying to open '+staticFileDir+'en/'+articleFolder+articleName)
		f = open(staticFileDir+'en/'+articleFolder+articleName,'w')
		print(new_soup,file=f)
		f.close
		print('Static save successful!')
	except:
		print('Trying to open '+staticFileDir+'en/'+articleFolder+articleName)
		print('Static save failed!!!')

	return

#Article counter
i=0

for infile in glob.glob( os.path.join('./wiki/liveArticles/', '*.html') ):
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

	articleTitle = articleTitle.translate(None, ",!.;[]\'\":-()*&^%$#@<>?{}=-_+`~")
	articleTitle = articleTitle.lower()
	articleFolder = articleTitle[0]+'/'+articleTitle[1]+'/'

	try:
		f = open(staticFileDir+'en/'+articleFolder+articleName,'r')
		print('Opening '+staticFileDir+'en/'+articleFolder+articleName+'...')
		for j, line in enumerate(f):
			if j == 1:	
				line = line.strip(' \t\n\r ')
				print(line)			
				if debug == True:
					f.close()
					print('Your wish is my command.')
					convertWikiArticle(infile)
				elif 'data-version=\"'+version+'\"' in line:


					print('Static version '+version+' already created!')
					f.close()
				else:
					f.close()
					print('Old file version. Converting file now.')
					convertWikiArticle(infile)	
			elif j > 1:
				break
		


	except:
		if not os.path.isfile(staticFileDir+'en/'+articleFolder+articleName):
			#articleName = articleName.encode('utf-8')
			print(staticFileDir+'en/'+articleFolder+articleName+' doesn\'t exist!')
			print('Converting file now')
			convertWikiArticle(infile)	



