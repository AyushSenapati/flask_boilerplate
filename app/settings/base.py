"""
Base settings module for the Flask application
"""
import os
import sys


BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASEDIR)

# Add all the services to this list,
# The blue prints of the services will automatically
# be registered under appropriate service tag
INSTALLED_SERVICES = [
    'service_test'
]

# DB settings
# Example_DB_URI = "postgresql+psycopg2://usr_name:passwd@host:5432/db_name"
SQLALCHEMY_DATABASE_URI = os.environ.get('SERVICE_TEST_DB')

# These binds must be used carefully with app models
SQLALCHEMY_BINDS = {
    'service_test_db': SQLALCHEMY_DATABASE_URI,
    # More binds can be added here
}

# Turn it off if you are not using flask-sqlalchemy signaling
SQLALCHEMY_TRACK_MODIFICATIONS = False
