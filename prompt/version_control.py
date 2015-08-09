"""
Contains methods for dealing with version control systems.
"""
from subprocess import check_output, CalledProcessError
import subprocess
from mercurial.error import RepoError
import sys

from exc import NoRepositoryException, VCSModuleMissingException


class Mercurial:
    def __init__(self):
        try:
            if 'mercurial' in sys.modules:
                from mercurial import ui, hg
            else:
                raise VCSModuleMissingException('Could not load mercurial module.')
            self.repo = hg.repository(ui.ui(), '.')
        except RepoError as rep_err:
            raise NoRepositoryException(rep_err.message)

    def branch(self):
        branch_name = self.repo.dirstate.branch()
        return branch_name.strip()

    def repository(self):
        repo_dir = self.repo.root
        return repo_dir.strip()

    def status(self):
        # Fields are: modified, added, removed, deleted, unknown, ignored, clean
        status = self.repo.status()
        if status.modified or status.added or status.removed or status.deleted:
            status_symbol = "!"
        elif status.unknown:
            status_symbol = "?"
        else:
            status_symbol = ""
        return status_symbol


class Git:
    def __init__(self):
        try:
            check_output(['git', 'rev-parse', '--git-dir'], stderr=subprocess.STDOUT)
        except CalledProcessError as e:
            raise NoRepositoryException(e.message)

    def branch(self):
        branch_name = check_output(['git', 'rev-parse', '--abbrev-ref', '@'], stderr=subprocess.STDOUT)
        return branch_name.strip()

    def repository(self):
        repo_dir = check_output(['git', 'rev-parse', '--show-toplevel'], stderr=subprocess.STDOUT)
        return repo_dir.strip()

    def status(self):
        status_out = check_output(['git', 'diff-index', '--name-status', '@', '--ignore-submodules'],
                                  stderr=subprocess.STDOUT)
        status_symbol = "!" if status_out else ""
        return status_symbol


class VersionControlProxy:
    """
    A proxy for version control tools. Contains a set of possible tools (git, mercurial, etc) and chooses which one to
    get information from based on the current directory.
    """

    def __init__(self):
        self.current_vcs = None
        self.set_current_vcs()

    def set_current_vcs(self):
        self.current_vcs = None
        for vcs in [Git, Mercurial]:
            try:
                self.current_vcs = vcs()
            except NoRepositoryException:
                continue
            else:
                return

    def branch(self, cache=True):
        if cache:
            pass
        if self.current_vcs is None:
            raise NoRepositoryException()
        return self.current_vcs.branch()

    def repository(self, cache=True):
        if cache:
            pass
        if self.current_vcs is None:
            raise NoRepositoryException()
        return self.current_vcs.repository()

    def status(self, cache=True):
        if cache:
            pass
        if self.current_vcs is None:
            raise NoRepositoryException()
        return self.current_vcs.status()
