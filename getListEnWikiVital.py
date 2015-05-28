from __future__ import print_function
import urllib2
from bs4 import BeautifulSoup


f = open('lists/ListEnWikiVital.txt','w')

#urls = ['http://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Level/2']  # Single page where the 100 vital articles are linked

urls = ['http://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Expanded/People','http://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Expanded/History','http://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Expanded/Geography','http://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Expanded/Arts','http://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Expanded/Philosophy_and_religion','http://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Expanded/Everyday_life','http://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Expanded/Society_and_social_sciences','http://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Expanded/Biology_and_health_sciences','http://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Expanded/Physical_sciences','http://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Expanded/Technology','http://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Expanded/Mathematics'] #pulls the article links to the vital 9742, plus some misc. links


for url in urls:
	s = urllib2.urlopen(url).read()


	#with file('List of articles every Wikipedia should have_Expanded - Meta.html') as f:
	#    s = f.read()

	soup = BeautifulSoup(s)
	soup.prettify()


	for anchor in soup.findAll('a', href=True):
		if '/wiki/' in anchor['href'] and not ':' in anchor['href'] and not '//' in anchor['href'] and not 'Main_Page' in anchor['href']:  # keeps the links mostly limited to Wikipedia articles
			print(anchor['href'],file=f)

f.close
