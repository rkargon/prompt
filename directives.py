from datetime import datetime
import os
from subprocess import CalledProcessError
from exc import DirectiveExpansionException

from version_control import branch


def color_directive(attribute):
    if attribute == "black":
        return "\033[30m"
    elif attribute == "red":
        return "\033[31m"
    elif attribute == "green":
        return "\033[32m"
    elif attribute == "yellow":
        return "\033[33m"
    elif attribute == "blue":
        return "\033[34m"
    elif attribute == "magenta":
        return "\033[35m"
    elif attribute == "cyan":
        return "\033[36m"
    elif attribute == "white":
        return "\033[37m"
    elif attribute == "reset":
        return "\033[0m"
    else:
        raise DirectiveExpansionException('Invalid color attribute "%s"' % attribute)


def date_directive(attribute):
    return datetime.now()


def user_directive(attribute):
    return os.environ['USER']


def branch_directive(attribute):
    try:
        return branch()
    except CalledProcessError as e:
        raise DirectiveExpansionException(e.message)

directives = {
    'col': color_directive,
    'date': date_directive,
    'user': user_directive,
    'branch': branch_directive,
}