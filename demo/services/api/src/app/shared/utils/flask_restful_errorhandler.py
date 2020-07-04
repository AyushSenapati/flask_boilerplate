import traceback
import logging
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import HTTPException
from flask import jsonify
from flask_restful import Api
from marshmallow.exceptions import ValidationError

logger = logging.getLogger(__name__)


# Class to handle service specific global exception
class ExtendedAPI(Api):
    def handle_error(self, err):
        """
        This class overrides 'handle_error' method of 'Api' class ,
        to extend global exception handing functionality of 'flask-restful'
        and helps preventing writing unnecessary
        try/except block though out the application
        """
        logger.exception(err, stack_info=True)

        # Handle HTTPExceptions, the base exception for all Werkzeug exceptions
        if isinstance(err, HTTPException):
            return jsonify({
                'success': False,
                'message': getattr(
                    err, 'description', HTTP_STATUS_CODES.get(err.code, '')
                ),
                'data': {
                    'type': 'error',
                    'class': err.__class__.__name__,
                    'base': 'HTTPException',
                    'source': 'werkzeug'
                }
            }), err.code

        if isinstance(err, ValidationError):
            resp = {
                'success': False,
                'message': err.messages,
                'data': {
                    'type': 'error',
                    'class': 'ValidationError',
                    'source': 'Serializer'
                }
            }
            return jsonify(resp), 400
        # If msg attribute is not set,
        # consider it as Python core exception and
        # hide sensitive error info from end user
        if getattr(err, 'message', None):
            return jsonify({
                'success': False,
                'message': 'Server has encountered some error'
            }), 500
        # Handle application specific custom exceptions
        try:
            err.kwargs['message'] = err.kwargs['msg']
            del(err.kwargs['msg'])
        except KeyError:
            pass
        return jsonify(**err.kwargs), err.http_status_code
