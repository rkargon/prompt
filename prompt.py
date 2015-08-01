import sys


class ParseTree:
    def __init__(self):
        self._parent = None
        self._children = []
        self.string = ""

    def parent(self):
        return self._parent

    def degree(self):
        """
        The number of children this node has
        """
        return len(self._children)

    def add_child(self, subtree):
        """
        Add a child to this node.
        Returns the child.
        """
        subtree._parent = self
        self._children.append(subtree)
        return subtree

    def children(self):
        return self._children

    def pretty_print(self, prefix=None, root=False):
        """
        Prints a representation of this tree.
        """
        if prefix is None:
            root = True
            prefix = ""

        out_str = prefix
        if root:
            out_str += "\\"
        out_str += '--- '
        if self.string:
            out_str += '"%s"' % self.string
        else:
            out_str += '*'

        print out_str

        if not self._children:
            return

        for c in self._children[:-1]:
            c.pretty_print(prefix + "     |")
        self._children[-1].pretty_print(prefix + "     ", root=True)


class UnmatchedDelimitersError(Exception):
    """
    Thrown when the delimiters in an expression are unmatched
    """
    pass

class DirectiveExpansionException(Exception):
    """
    Thrown when a directive fails to expand.
    When parsing nested expressions, if an inner expression fails then the outer one will simply return ""
    """
    pass



def main(argv):
    if len(argv) != 2:
        return usage()
    pattern = argv[1]
    prompt = parse(pattern)
    sys.stdout.write(prompt)


def parse(pattern):
    parse_tree = generate_parse_tree(pattern)
    parse_tree.pretty_print()
    out_str = expand_directives(parse_tree)
    return out_str

def generate_parse_tree(pattern):
    """
    Generates a parse tree for a given pattern
    """

    root = ParseTree()
    current_node = root
    current_child = None

    for char in pattern:
        # create sub-tree for this directive
        if char == "{":
            current_node = current_node.add_child(ParseTree())
            current_child = current_node.add_child(ParseTree())
        # end sub tree, return to parent
        elif char == "}":
            current_node = current_node.parent()
            if current_node is None:
                raise UnmatchedDelimitersError('Too many closing delimiters in pattern "%s"' % pattern)
            current_child = None
        # add character to this node's string value
        else:
            if current_child is None:
                current_child = current_node.add_child(ParseTree())
            current_child.string += char

    if current_node != root:
        raise UnmatchedDelimitersError('Too many opening delimiters in pattern "%s"' % pattern)
    return root

def expand_directives(parse_tree):
    if parse_tree.string:
        return parse_tree.string
    else:
        out_str = ""
        try:
            for c in parse_tree.children():
                out_str += expand_directives(c)
        except DirectiveExpansionException:
            return ""
        return evaluate_directive(out_str)

def evaluate_directive(out_str):
    return "[[" + out_str + "]]"

def usage():
    print "prompt.py <pattern>"
    print " - prints <pattern> to stdout"


if __name__ == '__main__':
    main(sys.argv)
