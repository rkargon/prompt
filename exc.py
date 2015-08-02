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