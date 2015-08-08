"""
Contains methods for dealing with version control systems.
"""
from subprocess import check_output, CalledProcessError
import subprocess

from exc import NoRepositoryError


class Mercurial:
    def __init__(self):
        pass

    @classmethod
    def test(cls):
        try:
            check_output(['hg', 'root'], stderr=subprocess.STDOUT)
            return True
        except CalledProcessError:
            return False

    @classmethod
    def branch(cls):
        branch_name = check_output(['hg', 'branch'], stderr=subprocess.STDOUT)
        return branch_name.strip()

    @classmethod
    def repository(cls):
        repo_dir = check_output(['hg', 'root'], stderr=subprocess.STDOUT)
        return repo_dir.strip()

    @classmethod
    def status(cls):
        status_out = check_output(['hg', 'status'], stderr=subprocess.STDOUT)
        status_symbol = "!" if status_out else ""
        return status_symbol


class Git:
    def __init__(self):
        pass

    @classmethod
    def test(cls):
        try:
            check_output(['git', 'rev-parse', '--git-dir'], stderr=subprocess.STDOUT)
            return True
        except CalledProcessError:
            return False

    @classmethod
    def branch(cls):
        branch_name = check_output(['git', 'rev-parse', '--abbrev-ref', '@'], stderr=subprocess.STDOUT)
        return branch_name.strip()

    @classmethod
    def repository(cls):
        repo_dir = check_output(['git', 'rev-parse', '--show-toplevel'], stderr=subprocess.STDOUT)
        return repo_dir.strip()

    @classmethod
    def status(cls):
        status_out = check_output(['git',  'diff-index',  '--name-status',  '@', '--ignore-submodules'],
                                  stderr=subprocess.STDOUT)
        status_symbol = "!" if status_out else ""
        return status_symbol


class VersionControlProxy:
    """
    A proxy for version control tools. Contains a set of possible tools (git, mercurial, etc) and chooses which one to
    get information from based on the current directory.
    """
    GIT = Git
    MERCURIAL = Mercurial
    VCS_TOOLS = [GIT, MERCURIAL]

    def __init__(self, vcs_name=None):
        if vcs_name is not None:
            pass
        else:
            self.current_vcs = None
            self.set_current_vcs()

    def set_current_vcs(self):
        self.current_vcs = None
        for vcs in self.VCS_TOOLS:
            if vcs.test():
                self.current_vcs = vcs

    def branch(self, cache=True):
        if cache:
            pass
        if self.current_vcs is None:
            raise NoRepositoryError()
        return self.current_vcs.branch()

    def repository(self, cache=True):
        if cache:
            pass
        if self.current_vcs is None:
            raise NoRepositoryError()
        return self.current_vcs.repository()

    def status(self, cache=True):
        if cache:
            pass
        if self.current_vcs is None:
            raise NoRepositoryError()
        return self.current_vcs.status()
