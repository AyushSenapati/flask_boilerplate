from flask_restful import Resource


class ControllerTest(Resource):
    def get(self):
        return {
            'message': 'Hello world!'
        }, 200
