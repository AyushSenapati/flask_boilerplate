"""
Module contains Resources for user management
"""
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

# Application level imports
from app.services.service_user_mgmt.utils import UserManager


class Users(Resource):
    method_decorators = [jwt_required]

    def get(self):
        """
        List users. Can also be used to
        search users based on certain filters
        """
        resp = {}

        parsed_args = UserManager.process_query_param(
            query_param=request.args
        )
        data = UserManager.list_users(parsed_args)
        resp['data'] = data
        return resp

    def post(self):
        """
        Create new User
        """
        resp = {}

        user_data = request.get_json(force=True)
        um = UserManager(data=user_data)
        user_data = um.create_user()
        resp['message'] = 'User created successfully'
        resp['data'] = user_data
        return resp, 200


class UserDetails(Resource):
    method_decorators = [jwt_required]

    def get(self, id):
        """
        Fetch information about a specific user.
        """
        resp = {}
        status = 400
        user = UserManager.get_user_by(field='id', value=id)
        if user:
            status = 200
            resp['data'] = user
        else:
            resp['message'] = f'User with ID {id} not found'
        return resp, status

    def put(self, id):
        """
        Update a specific user.
        """
        resp = {}
        status = 400

        user_data = request.get_json(force=True)
        um = UserManager(data=user_data, target='update')
        result = um.update_user(id)
        if result:
            resp['message'] = 'User details updated successfully!'
            resp['data'] = result
            status = 200
        else:
            resp['message'] = 'User updation failed'
            status = 500
        return resp, status

    def delete(self, id):
        """
        Delete a specific user.
        """
        resp = {}
        status = 400

        if UserManager.delete_user(id):
            resp['message'] = f'User with ID: {id} deleted successfully'
            status = 200
        else:
            resp['message'] = f'Failed to the delete the user with ID: {id}'
            status = 500
        return resp, status
