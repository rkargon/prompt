from subprocess import check_output, CalledProcessError
import subprocess


def branch():
    try:
        branchname = check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stderr=subprocess.STDOUT)
    except CalledProcessError as e:
        branchname = check_output(['hg', 'branch'], stderr=subprocess.STDOUT)
    return branchname
