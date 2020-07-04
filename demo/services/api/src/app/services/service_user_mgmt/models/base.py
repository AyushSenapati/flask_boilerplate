import logging

# Application level imports
from app import db
from app.shared.models.base import _Base

logger = logging.getLogger(__name__)


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base(cls=_Base)
