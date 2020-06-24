from functools import wraps
from flask_jwt_extended import (
    JWTManager, verify_jwt_in_request, get_jwt_claims)

# Application level imports
from ..exceptions.controllers import AuthorizationError


class CustomJWT(JWTManager):
    def __init__(self, app=None):
        """
        pass a flask application in directly here to register
        this extension with the flask app, or call init_app
        after creating this object

        """
        super().__init__(app=app)

    def init_app(self, app, blacklist_store):
        """
        Register this extension with the flask app.

        :param app: A flask application
        @param blacklist_store: storage object to check for black listed tokens
        """
        super().init_app(app)
        self.blacklist_store = blacklist_store

        # Callback will be called when
        # :func:`~flask_jwt_extended.create_access_token` is called.
        # It defines what custom claims should be added to the access token
        self.user_claims_loader(self.add_claims_to_access_token)

        # Callback will be called when
        # :func:`~flask_jwt_extended.create_access_token` is called.
        # It defines what the identity of the access token should be
        self.user_identity_loader(self.get_identity)
        self.token_in_blacklist_loader(self.check_if_token_in_blacklist)

    def get_identity(self, identity):
        if type(identity) == int:
            return identity
        return identity.id

    def add_claims_to_access_token(self, usr_obj):
        return {
            'id': usr_obj.id,
            'name': usr_obj.name,
            'role': {
                'id': usr_obj.role.id,
                'name': usr_obj.role.name
            }
        }

    def check_if_token_in_blacklist(self, decrypted_token):
        jti = decrypted_token['jti']
        # If entry found, then consider the token as revoked
        entry = self.blacklist_store.get(jti)
        if entry:
            return True
        return False  # Allow the token


def allow_roles(roles=[]):
    def decorated(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt_claims()
            # Check if claim is present in the accesstoken
            if not claims.get('role'):
                return {
                    'message': 'Malformed token',
                    'data': {
                        'type': 'error',
                        'class': AuthorizationError.__name__
                    }
                }, 401
            if claims['role']['name'] not in roles:
                return {
                    'message': 'Insufficient permission!!!',
                    'data': {
                        'type': 'error',
                        'class': AuthorizationError.__name__
                    }
                }, 403
            else:
                return fn(*args, **kwargs)
        return wrapped
    return decorated
