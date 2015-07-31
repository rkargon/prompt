import sys

def main(argv):
	if len(argv) != 2:
		return usage()
	pattern = argv[1]
	prompt = parse(pattern)
	sys.stdout.write(prompt)

def parse(pattern):
	# TODO actually do something
	return pattern

def usage():
	print "prompt.py <pattern>"
	print " - prints <pattern> to stdout"

if __name__ == '__main__':
	main(sys.argv)