from .base import Error


class QueryParseError(Error):
    """Should be raised in case of exception while parsing query parameters"""
