"""
Module contains logics for authentication system
"""
import traceback
import logging
from time import time
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    get_jwt_identity, get_raw_jwt, get_jwt_claims
)
from flask import current_app

# Application level import
from app import revoked_store
from app.services.service_user_mgmt.models import User

logger = logging.getLogger(__name__)


class AuthManager(object):
    def __init__(self, unmarshalled_data: dict = None):
        self.unmarshalled_data = unmarshalled_data
        self.authenticated = False

    def authenticate(self):
        """
        Fetches user using email and verifies the given password
        @return bool True on successful
                verification else False will be returned.
        """
        self.u_obj = User.get_user_by_email(self.unmarshalled_data['email'])
        self.authenticated = self.u_obj.verify_password(
            self.unmarshalled_data['password']
        )
        return self.authenticated

    def get_tokens(self) -> dict:
        """
        Checks if the user is authenticated and returns
        access and refresh tokens along with their type and header name
        on successful authentication.
        """
        if not self.authenticated:
            return {}

        _identity = self.u_obj

        # Create and return JWTs
        return {
            'access_token': create_access_token(identity=_identity),
            'expires_in': current_app.config['ACCESS_EXPIRES'].seconds,
            'token_type': current_app.config['JWT_HEADER_TYPE'],
            'auth_header': current_app.config['JWT_HEADER_NAME'],
            'refresh_token': create_refresh_token(identity=_identity)
        }

    @staticmethod
    def revoke_token(token_type='refresh'):
        """
        Method responsible for blacklisting tokens.
        Currently it only supports blacklisting refresh tokens.

        @return bool True: if token revoked successfully
                    False: Failed to revoke the token
        """
        try:
            raw = get_raw_jwt()
            jti = raw['jti']
            exp = raw['exp']
            time_diff = exp - int(time())
            revoked_store.set(jti, time_diff, time_diff)
        except Exception as e:
            logger.error(e, exc_info=traceback.format_exc())
            return False
        else:
            return True

    @staticmethod
    def get_access_using_refresh_token():
        """
        Method responsible for generating accesstoken using refresh token

        @return : None is returned in case of exception, else accesstoken
                will be returned.
        """
        try:
            current_user = get_jwt_identity()
            _claim = get_jwt_claims()
            access_token = create_access_token(
                identity=current_user,
                user_claims=_claim
            )
        except Exception as e:
            logger.error(e, exc_info=traceback.format_exc())
            return None
        else:
            return access_token
