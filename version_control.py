from subprocess import check_output, CalledProcessError
import subprocess


def branch():
    try:
        branch_name = check_output(['git', 'rev-parse', '--abbrev-ref', '@'], stderr=subprocess.STDOUT)
    except CalledProcessError:
        branch_name = check_output(['hg', 'branch'], stderr=subprocess.STDOUT)
    return branch_name.strip()


def status():
    try:
        status_out = check_output(['git',  'diff-index',  '--name-status',  '@', '--ignore-submodules'],
                              stderr=subprocess.STDOUT)
    except CalledProcessError:
        status_out = check_output(['hg', 'status'])

    status_symbol = ""
    if status_out:
        status_symbol = "!"
    return status_symbol

