import sys

class ParseTree:
	def __init__(self):
		self._parent = None
		self._children = []
		self.string = ""

	def add_child(self, subtree):
		subtree._parent = self
		self._children += subtree

def main(argv):
	if len(argv) != 2:
		return usage()
	pattern = argv[1]
	prompt = parse(pattern)
	sys.stdout.write(prompt)

def parse(pattern):
	parse_tree = generate_parse_tree(pattern)
	out_str = expand_directives(parse_tree)
	return pattern

def generate_parse_tree(pattern):
	root = ParseTree()
	current_node = root
	for char in pattern:
		if char == "{":
			child_node = ParseTree(current_node)
			current_node
		elif char == "}":
			pass
		else:
			current_node.string += char
	pass

def expand_directives(parse_tree):
	pass

def usage():
	print "prompt.py <pattern>"
	print " - prints <pattern> to stdout"

if __name__ == '__main__':
	main(sys.argv)