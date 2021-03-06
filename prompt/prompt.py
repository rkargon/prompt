import argparse
import os
import sys
import re

from directives import directives
from exc import DirectiveExpansionException
from parse_tree import ParseTree
from version_control import VersionControlProxy


class Prompt:
    def __init__(self, escape_colors=False):
        self.escape_colors=escape_colors
        self.vcs = VersionControlProxy()

    def parse(self, pattern):
        parse_tree = ParseTree.generate_parse_tree(pattern)
        # Don't parse root directly, because otherwise it would be treated as if the whole string were enclosed in {},
        # and any failing directive would cause the whole pattern to produce an empty string.
        out_str = ""
        for c in parse_tree.children():
            try:
                out_str += self.expand_directives(c)
            except DirectiveExpansionException:
                continue

        return out_str

    def expand_directives(self, parse_tree):
        if parse_tree.string:
            return parse_tree.string
        else:
            out_str = ""
            for c in parse_tree.children():
                out_str += self.expand_directives(c)
            return self.evaluate_directive(out_str)

    def evaluate_directive(self, directive):
        directive_regex = r"([^|]+)((?:\|([^|]+))*)"
        m = re.match(directive_regex, directive)
        if m is None:
            return directive
        else:
            name = m.group(1)
            args = m.group(2).split("|")
            args = filter(None, args)
        try:
            output = directives[name](args=args, vcs=self.vcs, escape_colors=self.escape_colors)
        except KeyError:
            return directive
        else:
            return str(output)


def main(argv):
    parser = argparse.ArgumentParser(description='A tool for customizing terminal prompts')
    parser.add_argument('-e', '--escape-colors', dest='escape_colors', action='store_const', const=True, default=False,
                        help='Escape colors codes with \[ and \] to help text wrapping. '
                             'Used when passing prompt output to PS1')
    parser.add_argument('pattern', metavar='pattern', type=str, help='The pattern for prompt to expand.')
    args = parser.parse_args()
    escape_colors = args.escape_colors
    pattern = args.pattern
    # reset text color after prompt is finished.
    pattern += '{col|reset}'

    prompt = Prompt(escape_colors=escape_colors)
    prompt_text = prompt.parse(pattern)
    sys.stdout.write(prompt_text)


def usage():
    print "prompt.py <pattern>"
    print " - prints <pattern> to stdout"


if __name__ == '__main__':
    main(sys.argv)
