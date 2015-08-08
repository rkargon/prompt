import os
from subprocess import check_output, CalledProcessError
import subprocess


def branch():
    try:
        branch_name = check_output(['git', 'rev-parse', '--abbrev-ref', '@'], stderr=subprocess.STDOUT)
    except CalledProcessError:
        branch_name = check_output(['hg', 'branch'], stderr=subprocess.STDOUT)
    return branch_name.strip()


def repository():
    try:
        repo_dir = check_output(['git', 'rev-parse', '--show-toplevel'], stderr=subprocess.STDOUT)
    except CalledProcessError:
        repo_dir = check_output(['hg', 'root'], stderr=subprocess.STDOUT)
    return repo_dir.strip()


def status():
    try:
        status_out = check_output(['git',  'diff-index',  '--name-status',  '@', '--ignore-submodules'],
                                  stderr=subprocess.STDOUT)
    except CalledProcessError:
        status_out = check_output(['hg', 'status'], stderr=subprocess.STDOUT)

    status_symbol = ""
    if status_out:
        status_symbol = "!"
    return status_symbol
