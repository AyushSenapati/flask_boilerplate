from functools import wraps
from flask import request, current_app


def api_key_required(f):
    """
    A decorator to protect the endpoint with api-key.

    If you decorate an endpoint with this, it will ensure that the requester
    has a valid api key before allowing the endpoint to be called.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        resp = {}
        status = 401
        api_key = request.headers.get('Api-Key', None)
        if api_key:
            if api_key != current_app.config.get('API_SVC_API_KEY'):
                status = 403
                resp['message'] = \
                    "Unauthorized Request. Invalid 'Api-Key' provided in the Headers."
                return resp, status
            return f(*args, **kwargs)
        else:
            resp['message'] = "Unauthorized Request. Missing 'Api-Key' in the Headers."
            return resp, status
    return wrapper
