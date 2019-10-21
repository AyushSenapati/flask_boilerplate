from app import db

from app.services.shared.models.base import BaseModel


class Base(BaseModel):
    '''
    This is an abstrct model. Upon inheriting this model
    few common fields and functionalities will be added to the child model.

    NOTE: This Base model needs to be imported in the alembic env.py file
    in order to detect schema changes automatically by sqlalchemy_migration.
    '''
    # WARNING: only the binds configured in SQL_ALCHEMY_BINDS
    # in the settings file can be used with __bind_key__
    __bind_key__ = 'service_test_db'

    __abstract__ = True
