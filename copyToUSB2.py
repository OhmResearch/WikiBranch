import os, shutil

file_paths = [os.path.join(root,f) for root, _, files in os.walk('wiki/fr/') for f in files]
for path in file_paths:
	print path
	try:
		if not os.path.exists('/run/media/user/LBOX21/LibraryBox/Shared/'+os.path.dirname(path)):
			os.makedirs('/run/media/user/LBOX21/LibraryBox/Shared/'+os.path.dirname(path))
		shutil.copy(path, '/run/media/user/LBOX21/LibraryBox/Shared/'+path)
	except:
		print "Error with: "+path
		with open("copy_fails.txt", "a") as f:
			f.write(path+'/n')


