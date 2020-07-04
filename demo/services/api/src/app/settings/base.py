"""
Base settings module for the Flask application
"""
import os
import sys
import logging
from logging import config
from datetime import timedelta


BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASEDIR)

# Provide absolute path to the config file
logger_config_file = BASEDIR + '/settings/logger.ini'

# Configure the logger for the application
config.fileConfig(logger_config_file)
_log_level = os.environ.get('LOG_LEVEL')
if not _log_level:
    _log_level = 'info'
try:
    logging.getLogger().setLevel(
        getattr(logging, _log_level.upper())
    )
except AttributeError:
    raise ValueError('Invalid log level!!!')

# Setup the flask-jwt-extended extension
# --------------------------------------
_jwt_secret = 'topsecret'
ACCESS_EXPIRES = timedelta(minutes=15)
REFRESH_EXPIRES = timedelta(days=1)
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', _jwt_secret)
if JWT_SECRET_KEY == _jwt_secret:
    print("[WARNING] JWT_SECRET_KEY is not set!!! using less secured key")
JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
JWT_REFRESH_TOKEN_EXPIRES = REFRESH_EXPIRES
# Enable to add claims to refresh token as well
JWT_CLAIMS_IN_REFRESH_TOKEN = True
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['refresh']

# Add all the services and their blueprints here
# ex: {'service_name': ListOfBlueprints}
INSTALLED_SERVICES = {
    'service_user_mgmt': ['service_user_mgmt_bp_v1'],
}

# DB settings
# -----------
# Example_DB_URI = "postgresql+psycopg2://usr_name:passwd@host:5432/db_name"
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
if not SQLALCHEMY_DATABASE_URI:
    print('[WARNING] SQLALCHEMY_DATABASE_URI is not set')

# Extracting redis connection details
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
REDIS_DB_NAME = os.environ.get('REDIS_DB_NAME', '0')
REDIS_BLACKLIST_URI = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NAME}'

# These binds must be used carefully with app models
# SQLALCHEMY_BINDS = {
#     'service_user_mgmt': os.environ.get('SERVICE_USER_MGMT_DB'),
#     # More binds can be added here
# }

# Turn it off if you are not using flask-sqlalchemy signaling
SQLALCHEMY_TRACK_MODIFICATIONS = False
