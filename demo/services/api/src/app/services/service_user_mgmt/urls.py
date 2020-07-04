from flask import Blueprint, jsonify
from marshmallow.exceptions import ValidationError

# Application level import
from app.shared.utils.flask_restful_errorhandler import ExtendedAPI

# Import controllers to create routes
from app.services.service_user_mgmt.controllers.v1 import auth, user, role

# Similarly you can add another api version
# ex: service_user_mgmt_bp_v2 = Blueprint('service_user_mgmt2', __name__)
service_user_mgmt_bp_v1 = Blueprint('service_user_mgmt1', __name__)
service_user_mgmt_api_v1 = ExtendedAPI(
    service_user_mgmt_bp_v1, prefix='/v1', catch_all_404s=True)

# Service specific routes goes here
# EX: service_user_mgmt_api_v1.add_resource(ControllerName, '/route')

# Auth controllers
service_user_mgmt_api_v1.add_resource(auth.UserLogin, '/auth/login')
service_user_mgmt_api_v1.add_resource(auth.TokenRefresh, '/auth/refresh')
service_user_mgmt_api_v1.add_resource(auth.RefreshTokenRevoke, '/auth/logout')
# User controllers
service_user_mgmt_api_v1.add_resource(user.Users, '/users')
service_user_mgmt_api_v1.add_resource(user.UserDetails, '/users/<int:id>')

# list roles
service_user_mgmt_api_v1.add_resource(role.Roles, '/roles')
