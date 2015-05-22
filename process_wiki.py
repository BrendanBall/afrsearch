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

def scrub(min_lines=20):
	remove = []
	image_ext = [".jpg", ".jpeg", ".gif", ".png", ".svg"]
	bad_titles = [
			"Bespreking",
			"Gebruiker",
			"Kategorie",
			"Sjabloon",
			"_v.C._",
			"Lys_van_",
			"Januarie",
			"Februarie",
			"Maart",
			"April",
			"Mei",
			"Junie",
			"Julie",
			"Augustus",
			"September",
			"Oktober",
			"November",
			"Desember",
			"Wikipedia~"
			]

	for fname in os.listdir("output"):
		# remove image pages
		for ext in image_ext:
			if ext in fname:
				remove.append(fname)
				continue
		
		# remove year pages
		if fname[:-4].isdigit():
			remove.append(fname)
			continue

		# remove other meta pages
		for t in bad_titles:
			if t in fname:
				remove.append(fname)
				continue

		# remove the last lines containing links etc
		with open("output/%s" % fname) as f:
			lines = f.readlines()

		cutoff = len(lines) - 1
		while cutoff > 0:
			if lines[cutoff].startswith("Views"):
				break
			cutoff-=1

		if cutoff > 0:
			lines = lines[:cutoff]

		# remove small articles
		if len(lines) < min_lines:
			remove.append(fname)
			continue

		# get rid of the tag line, and any "small articles"
		for line in lines:
			if line.startswith("vanuit Wikipedia, die vrye ensiklopedie."):
				lines.remove(line)
			elif line.startswith("Hierdie artikel is 'n saadjie"):
				remove.append(fname)
				continue

		with open("output/%s" % fname, "w") as f:
			f.writelines(lines)

	for fname in remove:
		if os.path.exists("output/%s" % fname):
			print "Removing %s" % fname
			os.remove("output/%s" % fname)

	
if __name__ == "__main__":
	help_string = "Usage: python process_wiki.py [wiki dump dir]"

	if len(sys.argv) < 2:
		print help_string
		sys.exit()

	if not os.path.isdir("output"):
		os.mkdir("output")

	# process_files(find_files(sys.argv[1]))
	scrub()

