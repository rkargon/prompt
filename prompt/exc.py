class ParseError(Exception):
    """
    Thrown then where is some error in parsing the prompt
    """
    pass


class UnmatchedDelimitersError(ParseError):
    """
    Thrown when the delimiters in an expression are unmatched
    """
    pass


class DirectiveExpansionException(ParseError):
    """
    Thrown when a directive fails to expand.
    When parsing nested expressions, this exception is caught.
    If an inner expression fails then the outer one will simply return ""
    """
    pass


class NoRepositoryException(DirectiveExpansionException):
    """
    Thrown when a vcs command is parsed, but the current directory is not part of a version control repo.
    """
    pass


class VCSModuleMissingException(DirectiveExpansionException):
    """
    Thrown when the modules for a certain VCS system could not be loaded.
    (e.g. if mercurial is not installed on a system)
    """
    pass
