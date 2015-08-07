from datetime import datetime
import os
import socket
from subprocess import CalledProcessError
from exc import DirectiveExpansionException
from version_control import branch, status, repository


def color_directive(args):
    colname = args[0]
    if colname == "black":
        return "\033[30m"
    elif colname == "red":
        return "\033[31m"
    elif colname == "green":
        return "\033[32m"
    elif colname == "yellow":
        return "\033[33m"
    elif colname == "blue":
        return "\033[34m"
    elif colname == "magenta":
        return "\033[35m"
    elif colname == "cyan":
        return "\033[36m"
    elif colname == "white":
        return "\033[37m"
    elif colname == "reset":
        return "\033[0m"
    else:
        raise DirectiveExpansionException('Invalid color attribute "%s"' % colname)


def date_directive(args):
    return datetime.now()


def host_directive(args):
    return socket.gethostname()


def user_directive(args):
    return os.environ['USER']


def working_dir_directive(args):
    return os.path.basename(os.getcwd())


def branch_directive(args):
    try:
        return branch()
    except CalledProcessError as e:
        raise DirectiveExpansionException(e.message)


def repo_directive(args):
    """
    Returns the name of the repository's root directory.
    """
    try:
        return repository()
    except CalledProcessError as e:
        raise DirectiveExpansionException(e.message)


def status_directive(args):
    try:
        return status()
    except CalledProcessError as e:
        raise DirectiveExpansionException(e.message)

directives = {
    'col': color_directive,
    'date': date_directive,
    'host': host_directive,
    'user': user_directive,
    'cwd': working_dir_directive,
    'branch': branch_directive,
    'repo': repo_directive,
    'status': status_directive,
}