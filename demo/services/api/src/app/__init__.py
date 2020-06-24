"""Module contains the factory method
to instantiate Flask application
"""

import os
# used to import modules dynamically
from importlib import import_module

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_migrate import Migrate
from flask import g

# Application level imports
from .shared.utils.redis_util import FlaskRedis

# Instatiate the extensions
cors = CORS()
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
revoked_store = FlaskRedis(config_prefix='REDIS_BLACKLIST')


def create_app(env='development'):
    # Instatiate the Flask app
    app = Flask(__name__)

    # Load app settings
    app_settings = f"app.settings.{os.environ.get('FLASK_ENV', env)}"
    if 'development' in app_settings:
        print("[WARNING] Using development environment")
    app.config.from_object(app_settings)

    # Set up extensions
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    revoked_store.init_app(app)
    migrate.init_app(app, db=db)

    from .shared.utils.jwt_initializer import CustomJWT

    jwt = CustomJWT()
    jwt.init_app(app, revoked_store)

    # Register blueprints of all the services mentioned
    # in the app settings to the flask instance
    for service in app.config['INSTALLED_SERVICES'].keys():
        fqs_path = f"app.services.{service}"
        module = import_module('.urls', package=fqs_path)
        for bp_name in app.config['INSTALLED_SERVICES'][service]:
            bp_obj = getattr(module, bp_name)
            app.register_blueprint(bp_obj, url_prefix=f'/api')

    # Shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    # Intersect the reponse and add request-id to the reponse header
    @app.after_request
    def add_request_id(response):
        response.headers.add('X-REQUEST-ID', g.get('request_id'))
        return response

    @app.route('/health', methods=['GET'])
    def health_check():
        """
        This is the Pitta health check API.
        Call this endpoint to check if the service is running or not
        """
        return 'Working!!!'

    return app
