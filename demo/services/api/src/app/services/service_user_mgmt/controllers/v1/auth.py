"""
Module contains authentication controllers
"""
import time
from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_refresh_token_required,
    get_jwt_identity,
    create_access_token,
    get_raw_jwt
)

# Application level imports
from app.services.service_user_mgmt.utils import (UserManager, AuthManager)


class UserLogin(Resource):
    def post(self):
        """
        Authenticates the user and returns access_token,
        refresh_token and user details
        """
        resp = {}

        credentials = request.get_json(force=True)
        um = UserManager(data=credentials, target='login')
        if um.auth.authenticate():
            resp['message'] = 'logged in successfully!'
            resp['data'] = um.auth.get_tokens()
            resp['data']['user'] = um.get_serialized_user()
            statuscode = 200
        else:
            resp['message'] = 'Login failed!!'
            statuscode = 400
        return resp, statuscode


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        """
        Gives the user a new access_token.
        Pass your refresh_token in header
        """
        resp = {
            'message': 'Failed to generate access token'
        }
        statuscode = 500
        access_token = AuthManager().get_access_using_refresh_token()
        if access_token:
            resp['message'] = 'Access_token generated'
            resp['data'] = {
                'access_token': access_token
            }
            statuscode = 200

        return resp, statuscode


class RefreshTokenRevoke(Resource):
    @jwt_refresh_token_required
    def delete(self):
        """
        Logs out a user. Pass your refresh_token in header
        """
        resp = {
            'message': 'Failed to logout! Please try again.',
        }
        statuscode = 500
        if AuthManager().revoke_token():
            resp['message'] = 'Refresh token has been revoked'
            statuscode = 200
        return resp, statuscode
