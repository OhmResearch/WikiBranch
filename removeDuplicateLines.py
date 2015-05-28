# you'll notice that after we generate a list of media files from the conversion of Wiki pages to static pages, there are tons of duplicates.
# we'd like to regenerate the list so that no duplicates are included
# script should only take about 0.1 seconds to complete

infilename = 'lists/listInfoBoxImgs.txt'
outfilename = 'lists/listInfoBoxImgs-nodup.txt'

lines_seen = set() # holds lines already seen
outfile = open(outfilename, "w")
for line in open(infilename, "r"):
    if line not in lines_seen: # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()