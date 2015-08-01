from datetime import datetime
import os

from version_control import branch


def date_directive(attribute):
    return datetime.now()


def user_directive(attribute):
    return os.environ['USER']


def branch_directive(attribute):
    return branch()

directives = {
    'date': date_directive,
    'user': user_directive,
    'branch': branch_directive,
}