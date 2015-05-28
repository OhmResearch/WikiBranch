from __future__ import print_function
import urllib2
from bs4 import BeautifulSoup

# File to dump the article link list
f = open('lists/listAddPortalArticles.txt','w')

#URLs for the Vital 100
#urls = ['http://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Level/2']  # Single page where the 100 vital articles are linked

#URLs for the Vital 10,000
#urls = ['http://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Expanded/People','http://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Expanded/History','http://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Expanded/Geography','http://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Expanded/Arts','http://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Expanded/Philosophy_and_religion','http://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Expanded/Everyday_life','http://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Expanded/Society_and_social_sciences','http://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Expanded/Biology_and_health_sciences','http://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Expanded/Physical_sciences','http://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Expanded/Technology','http://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Expanded/Mathematics'] #pulls the article links to the vital 9742, plus some misc. links

#URLs related to Rwanda
#urls = ['https://en.wikipedia.org/wiki/Portal:Rwanda','https://en.wikipedia.org/wiki/Portal:Rwanda/Featured_article','https://en.wikipedia.org/wiki/Portal:Rwanda/Featured_picture','https://en.wikipedia.org/wiki/Portal:Rwanda/Featured_biography']

#URLs from https://en.wikipedia.org/wiki/Portal:Contents
#urls = ['https://en.wikipedia.org/wiki/Portal:Contents/Reference','https://en.wikipedia.org/wiki/Portal:Contents/Culture_and_the_arts','https://en.wikipedia.org/wiki/Portal:Contents/Geography_and_places','https://en.wikipedia.org/wiki/Portal:Contents/Health_and_fitness','https://en.wikipedia.org/wiki/Portal:Contents/History_and_events','https://en.wikipedia.org/wiki/Portal:Contents/Mathematics_and_logic','https://en.wikipedia.org/wiki/Portal:Contents/Natural_and_physical_sciences','https://en.wikipedia.org/wiki/Portal:Contents/People_and_self','https://en.wikipedia.org/wiki/Portal:Contents/Philosophy_and_thinking','https://en.wikipedia.org/wiki/Portal:Contents/Religion_and_belief_systems','https://en.wikipedia.org/wiki/Portal:Contents/Society_and_social_sciences','https://en.wikipedia.org/wiki/Portal:Contents/Technology_and_applied_sciences'] 

#URLs from Africa portal
urls = []

#URLs from the 5000 most viewed pages of the week
#urls = ['https://en.wikipedia.org/wiki/User:West.andrew.g/Popular_pages']


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
