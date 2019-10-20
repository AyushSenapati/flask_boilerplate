"""Module contains the factory method
to intiantiate Flask application
"""

import os
# used to import modules dynamically
from importlib import import_module

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
from flask_migrate import Migrate


# Instatiate the extensions
db = SQLAlchemy()
migrate = Migrate()


def create_app(app_settings=None):
    # Instatiate the Flask app
    app = Flask(__name__)

    # Load app settings
    app_settings = f"app.settings.{os.environ.get('FLASK_ENV', 'development')}"
    app.config.from_object(app_settings)

    # Set up extensions
    db.init_app(app)
    migrate.init_app(app, db=db)

    # Auto register blueprints of installed services
    for service in app.config['INSTALLED_SERVICES']:
        # fully qualified service name and path
        fqs_path = f"app.services.{service}"
        fqs_name = f"{service}_bp"
        module = import_module('.urls', package=fqs_path)
        bp_obj = getattr(module, fqs_name)
        app.register_blueprint(bp_obj, url_prefix=f'/api/{service}')

    # Shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
