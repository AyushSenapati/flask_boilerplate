import traceback
import logging
import psycopg2
from sqlalchemy.exc import IntegrityError

# Application level imports
from app import db
from app.shared import exceptions as custom_exptn

logger = logging.getLogger(__name__)


class _Base(object):
    '''
    This is an abstrct model. Upon inheriting this model
    few common fields and functionalities will be added to the child model.
    '''
    __abstract__ = True

    created_at = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp(),
        nullable=False
    )
    updated_at = db.Column(
        db.TIMESTAMP,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
        nullable=False
    )

    def delete(self):
        """Deletes the resource object and saves the transaction"""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            logger.error(e, exc_info=traceback.format_exc())
            db.session.rollback()
            raise custom_exptn.models.DBError(
                500, msg="Failed to remove the resource",
                resource=self.__class__.__name__)
        else:
            return True

    def save_to_db(self, bulk_objs: list = [], return_defaults=False):
        try:
            if bulk_objs:
                db.session.bulk_save_objects(
                    bulk_objs, return_defaults=return_defaults)
                db.session.commit()
                if return_defaults:
                    return bulk_objs
            else:
                db.session.add(self)
                db.session.commit()
        except IntegrityError as e:
            logger.error(e, exc_info=traceback.format_exc())
            db.session.rollback()
            try:
                # Reraise the original DB exception
                # raised by the adapter, to generate
                # finegrained response messages
                raise e.orig
            except psycopg2.errors.UniqueViolation:
                raise custom_exptn.models.DBError(
                    400,
                    msg="Resource already exist with provided details",
                    data={
                        "type": "error",
                        "class": "IntegrityError",
                        "reason": "UniqueViolation",
                    }
                )
            except psycopg2.errors.ForeignKeyViolation as e:
                logger.exception(e)
                raise custom_exptn.models.DBError(
                    400,
                    msg='Given relational record not found',
                    data={
                        "type": "error",
                        "class": "IntegrityError",
                        "reason": "ForeignKeyViolation"
                    }
                )
            # Catch uncaught exceptions and log.
            # Make sure you check log periodically to find
            # all uncaught DB exceptions and handle
            # them properly to avoid global exception handling
            except Exception as e:
                logger.error(e, exc_info=traceback.format_exc())
                raise custom_exptn.models.DBError(
                    500, msg="Something went wrong! Please contact the Admin")
        # Catch all SqlAlchemy global exceptions
        # and eventually add handlers for them
        except Exception as e:
            logger.error(e, exc_info=traceback.format_exc())
            db.session.rollback()
            raise custom_exptn.base.ServerError(
                500, msg="Something went wrong! Please contact the Admin")

    @staticmethod
    def get_base_query(parsed_args):
        q = \
            "db.session.query(cls).order_by(" +\
            "getattr(cls, parsed_args['order_by_field']){order_by})" \
            .format(
                order_by='.desc()' if parsed_args['order_by'].lower() == 'desc' else ''
            )
        return q

    @classmethod
    def get_result(cls, query, parsed_args):
        if parsed_args['page']:
            query += ".paginate(" \
                "page=parsed_args['page'], max_per_page=parsed_args['max_per_page'])"
            # Page not found exception would be handled by the sqlalchemy
            logger.debug(f"QUERY: {query}")  # log the final query
            query_obj = eval(query)
            records = query_obj.items  # list of records
            result = {
                'records': records,  # records that needs to be serialized
                'current_page': query_obj.page,
                'total_pages': query_obj.pages,
                'total_records': query_obj.total
            }
        else:
            query_obj = eval(query)
            records = query_obj.all()
            result = {
                'records': records
            }
        return result

    @classmethod
    def get_by(cls, field, value, created_by=None):
        """Returns model object in case of no exception,
        else Resource not found custom exception will be raised
        """
        q = f"db.session.query(cls).filter(cls.{field}=='{value}')"
        if created_by and isinstance(created_by, int) and hasattr(cls, 'created_by'):
            q += f".filter(cls.created_by=={created_by})"
        q += '.first()'
        model_obj = eval(q)
        if not model_obj:
            raise custom_exptn.models.ResourceNotFound(
                404, msg=f"{cls.__name__} not found with {field}: {value}")
        return model_obj

    @classmethod
    def filter(cls, target=None, queries=[]):
        if not target:
            target = cls
        q = f"db.session.query(target)"
        # Append all the provided filters
        for query in queries:
            q += query
        return eval(q)
