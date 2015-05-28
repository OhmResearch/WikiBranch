import fnmatch
import os
import string
import shutil

searchStr = u"\u003F"

for root, dirnames, filenames in os.walk('./wiki/commons/'):
	for dirname in dirnames:
		if "?" in dirname or "\"" in dirname or "*" in dirname:
			print(root+'/'+dirname)
			shutil.rmtree(root+'/'+dirname)

