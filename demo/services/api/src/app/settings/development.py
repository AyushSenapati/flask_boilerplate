"""Inherits base setting file and
overwrites as needed for Dev env
"""

from app.settings.base import *

# SQLAlchemy settings for Dev env
SQLALCHEMY_ECHO = True
