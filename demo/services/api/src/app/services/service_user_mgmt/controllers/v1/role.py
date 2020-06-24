"""
Module contains Resources for user management
"""
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

# Application level imports
from app.services.service_user_mgmt.utils import UserManager
from app.shared.utils.jwt_initializer import allow_roles


class Roles(Resource):
    method_decorators = [jwt_required]

    @allow_roles(roles=['admin'])
    def get(self):
        resp = {
            'data': UserManager.list_roles()
        }
        return resp
