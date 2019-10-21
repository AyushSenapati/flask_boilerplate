
from flask import Blueprint
from flask_restful import Api

# Import controllers to create routes
from app.services.service_test.controllers.test import ControllerTest


# Class to handle service specific global exception
class ExtendedAPI(Api):
    def handle_error(self, err):
        pass


service_test_bp = Blueprint('service_test', __name__)
service_test_api = ExtendedAPI(service_test_bp)

# Service specific routes goes here
# EX: service_test_api.add_resource(ControllerName, '/route')
service_test_api.add_resource(ControllerTest, '/test')
