from .base import Error


class AuthorizationError(Error):
    """Should be raised in case of insufficient permission"""
    def __init__(self, *args, **kwargs):
        http_status_code = 403
        super().__init__(http_status_code, *args, **kwargs)
