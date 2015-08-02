from subprocess import check_output, CalledProcessError
import subprocess


def branch():
    try:
        branch_name = check_output(['git', 'rev-parse', '--abbrev-ref', '@'], stderr=subprocess.STDOUT)
    except CalledProcessError as e:
        branch_name = check_output(['hg', 'branch'], stderr=subprocess.STDOUT)
    return branch_name.strip()
