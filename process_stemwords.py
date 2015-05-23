import sys
import re

def main(path):
	with open(path) as f:
		raw = f.readlines()
	open("stem.txt", "w").close()
	with open("stem.txt", "a") as f:
		for line in raw:
			line = line[2:]
			line = line.replace("\n", "")
			line = re.sub("\([^\)]*\)", "", line)
			line = re.sub("\.\.\w+", "", line)
			line = re.sub("\w+\.\.", "", line)
			line = re.sub("(\,|\ )+\w+\ \*.*", "", line)
			line = re.sub(",\ -[^,]*", "", line)
			line = re.sub("(\,)+(\,|\ )*", ", ", line)


			if re.match("^\w+\ *\,*\ *$", line):
				continue

			print >>f, line

			

	


if __name__ == "__main__":
	main(sys.argv[1])
