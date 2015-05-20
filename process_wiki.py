import sys
import subprocess
import fnmatch
import os

def find_files(base):
	matches = []
	for root, dirnames, filenames in os.walk(base):
	  for filename in fnmatch.filter(filenames, '*.html'):
		matches.append(os.path.join(root, filename))
	
	return matches

def process_files(files):
	for in_file in files:
		basename = in_file[in_file.rfind("/"):]
		basename = basename[:basename.rfind(".")]+".txt"
		print "Processing %s" % in_file
		with open("output/%s" % basename, "w") as out_file:
			process(in_file, out_file)

def process(in_file, out_file):
    subprocess.call(['lynx', '-dump', '-nolist', in_file], stdout=out_file)

def scrub(min_lines=5):
	remove = []
	image_ext = ["jpg, jpeg, gif, png, svg"]

	for fname in os.listdir("output"):
		delete = False

		# remove image pages
		for ext in image_ext:
			if ext in fname:
				remove.append(fname)
				continue

		# remove small articles
		if os.stat("output/%s" % fname).st_size < 2048:
			remove.append(fname)
			continue

	for fname in remove:
		print "Removing %s" % fname
		os.remove("output/%s" % fname)

	
if __name__ == "__main__":
	help_string = "Usage: python process_wiki.py [wiki dump dir]"

	if len(sys.argv) < 2:
		print help_string
		sys.exit()

	if not os.path.isdir("output"):
		os.mkdir("output")

	process_files(find_files(sys.argv[1]))
	scrub()

