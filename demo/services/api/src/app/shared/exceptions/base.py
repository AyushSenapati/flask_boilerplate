"""
Module contains base Exception for the application.
"""
from flask import jsonify


class Error(Exception):
    """Base class for other exceptions"""
    def __init__(self, http_status_code: int, *args, **kwargs):
        # If the key `msg` is provided, provide the msg string
        # to Exception class in order to display
        # the msg while raising the exception
        self.http_status_code = http_status_code
        self.kwargs = kwargs
        self.kwargs['success'] = False
        msg = kwargs.get('msg', kwargs.get('message'))
        if msg:
            args = (msg,)
            super().__init__(args)
        self.args = list(args)
        if kwargs.get('data') is None:
            kwargs.update({
                'data': {
                    'type': 'error',
                    'class': self.__class__.__name__
                }
            })
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])

    def get_response(self):
        ret = dict(self.kwargs)
        ret['message'] = self.msg
        return jsonify(ret), self.http_status_code


class ServerError(Error):
    """Raise in case of Internal server error"""
