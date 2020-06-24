"""
Module contains model specific custom exceptions
"""
from flask import jsonify

# Application level imports
from .base import Error


class DBError(Error):
    """Parent custom DB Error"""


class ResourceNotFound(DBError):
    """Should be raised in case any resource is not found in the DB"""
