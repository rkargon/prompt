from datetime import datetime
import os
import socket
from subprocess import CalledProcessError
import re
from exc import DirectiveExpansionException


def color_directive(**kwargs):
    commands = {
        'reset': 0,

        # text styles
        'bold': 1,
        'italic': 3,
        'underline': 4,
        'bold_off': 22,
        'italic_off': 23,
        'underline_off': 24,

        # foreground (text) colors
        'black': 30,
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'magenta': 35,
        'cyan': 36,
        'white': 37,
        'fg_reset': 39,

        # background colors
        'bg_black': 40,
        'bg_red': 41,
        'bg_green': 42,
        'bg_yellow': 43,
        'bg_blue': 44,
        'bg_magenta': 45,
        'bg_cyan': 46,
        'bg_white': 47,
        'bg_reset': 49,
    }
    
    out_text = ""
    args = kwargs['args']
    for arg in args:
        if arg in commands:
            out_text += "\033[%dm" % commands[arg]
        elif re.match('[34]8;(?:2;\d+;\d+;\d+|5;\d+)', arg):
            print "make some noooooiissseee!"
            out_text += "\033[%sm" % arg

    return out_text


def date_directive(**kwargs):
    return datetime.now()


def host_directive(**kwargs):
    return socket.gethostname()


def user_directive(**kwargs):
    return os.environ['USER']


def working_dir_directive(**kwargs):
    cwd = os.getcwd()
    args = kwargs['args']
    if args and args[0] == 'short':
        cwd = os.path.basename(cwd)
    return cwd


def branch_directive(**kwargs):
    try:
        return kwargs['vcs'].branch()
    except CalledProcessError as e:
        raise DirectiveExpansionException(e.message)


def repo_directive(**kwargs):
    """
    Returns the name of the repository's root directory.
    """
    try:
        reponame = kwargs['vcs'].repository()
        args = kwargs['args']
        if args and args[0] == 'short':
            reponame = os.path.basename(reponame)
        return reponame
    except CalledProcessError as e:
        raise DirectiveExpansionException(e.message)


def status_directive(**kwargs):
    try:
        return kwargs['vcs'].status()
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