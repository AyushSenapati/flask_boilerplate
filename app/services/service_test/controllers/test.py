import logging
from flask_restful import Resource

logger = logging.getLogger(__name__)


class ControllerTest(Resource):
    def get(self):
        logger.info('it is working')
        return {
            'message': 'Hello world!'
        }, 200
