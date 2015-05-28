import os, random
import glob

i=0

for infile in glob.glob( os.path.join('./wiki/fr/', '*.html') ):
	i+=1

#print(i)	


cpt = sum([len(files) for r, d, files in os.walk("./wiki/commons/")])
print(cpt)