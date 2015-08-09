from datetime import datetime
import os
import socket
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
            out_text += "\033[%sm" % arg

    return out_text


def date_directive(**kwargs):
    return datetime.now()


def host_directive(**kwargs):
    return socket.gethostname()


def user_directive(**kwargs):
    return os.environ['USER']


def virtualenv_directive(**kwargs):
    try:
        return os.path.basename(os.environ['VIRTUAL_ENV'])
    except KeyError:
        raise DirectiveExpansionException('No current virtualenv')


def working_dir_directive(**kwargs):
    cwd = os.getcwd()
    args = kwargs['args']
    if args and args[0] == 'short':
        cwd = os.path.basename(cwd)
    return cwd


def branch_directive(**kwargs):
    return kwargs['vcs'].branch()


def repo_directive(**kwargs):
    """
    Returns the name of the repository's root directory.
    """
    reponame = kwargs['vcs'].repository()
    args = kwargs['args']
    if args and args[0] == 'short':
        reponame = os.path.basename(reponame)
    return reponame


def status_directive(**kwargs):
    return kwargs['vcs'].status()

directives = {
    'col': color_directive,
    'cwd': working_dir_directive,
    'date': date_directive,
    'host': host_directive,
    'user': user_directive,
    'virtualenv': virtualenv_directive,
    #version control
    'branch': branch_directive,
    'repo': repo_directive,
    'status': status_directive,
}