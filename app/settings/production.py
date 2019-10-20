"""Inherits base setting file and
overwrites as needed for Production env
"""

from app.settings.base import *

# SQLAlchemy settings for Dev env
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False