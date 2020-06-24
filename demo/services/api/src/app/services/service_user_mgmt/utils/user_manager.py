"""
Module provides a bridge between user controllers and models
"""
import logging

# Application level imports
from app.services.service_user_mgmt.models import (
    User, UserSchema, Role, RoleSchema
)
from app.shared.utils.query_parser import QueryParser
from .auth_manager import AuthManager

logger = logging.getLogger(__name__)

# Configure the UserSchema serializer
# instances for different operations
USER_SCHEMA_OBJS = {
    'default': UserSchema(),
    'login': UserSchema(
        only=('email', 'password'),
        unknown='INCLUDE'
    ),
    'update': UserSchema(
        only=('name', 'password', 'role_id'),
        unknown='INCLUDE',
        partial=True
    )
}

# Mention all the query parameters that the User manager
# allows with their data types. This dict will be used to convert
# query parameters to Python's native data type.
ALLOWED_KEYS_WITH_DTYPE = {
    'role_id': int,
    'name': str,
    'email': str,
}

DEFAULTS = {}


class UserManager(object):
    def __init__(self, data: dict = {}, target: str = 'default'):
        """Data manager to provide a bridge
        between user controllers and models layers.

        :param data: User input
        :param target: Serializer instance for different operations
        """
        if data:
            self.deserialized_data = self.deserialize(
                data, USER_SCHEMA_OBJS[target]
            )
        else:
            self.deserialized_data = {}
        self.auth = AuthManager(self.deserialized_data)

    def deserialize(self, data, usr_schema_obj):
        return usr_schema_obj.load(data)

    @classmethod
    def process_query_param(cls, **kwargs) -> ({}, []):
        qp_obj = QueryParser(
            extend_defaults=DEFAULTS,
            extend_allowed_keys_with_dtype=ALLOWED_KEYS_WITH_DTYPE
        )
        parsed_args = qp_obj.parse_query_param(**kwargs)
        return parsed_args

    @classmethod
    def list_users(cls, parsed_args: dict):
        """
        returns serialized paginated list of users

        :param parsed_args: Parsed query parameters
        :return: serialized paginated list of users
        """
        result = User.list_users(parsed_args)
        result['records'] = UserSchema(many=True).dump(result['records'])
        return result

    @classmethod
    def get_user_by(cls, field: str = 'id', value=None, serialized=True):
        if not value:
            raise ValueError
        u = User.get_by(field, value)
        if serialized:
            return UserSchema().dump(u)
        else:
            return u

    def create_user(self) -> dict:
        """
        Tries to create an user and save to the db

        :return:
            serialized user details. In case of exception,
            appropriate error response will be returned.
        """
        u = User(**self.deserialized_data)
        u.save_to_db()
        return UserSchema().dump(u)

    def update_user(self, uid: int) -> dict:
        """Updates User details.
        It only allows updation of name, password and role_id fields

        :param uid: User ID
        :return: Serialized User details
        """
        result = {}
        u_obj = User.get_by('id', uid)

        # Try to get parsed input and save the allowed fields
        for key in self.deserialized_data.keys():
            setattr(u_obj, key, self.deserialized_data.get(key))

        # Save the updated user object to DB
        u_obj.save_to_db()

        # Serialise User object and update the result dict,
        # which needs to be returned
        result.update(UserSchema().dump(u_obj))
        return result

    def get_serialized_user(self) -> dict:
        """Returns a serialized user
        object if the user is authenticated

        :return:
            Serialized user details
        """
        if not self.auth.authenticated:
            return {}
        return UserSchema().dump(self.auth.u_obj)

    @classmethod
    def delete_user(cls, uid: int) -> bool:
        """Helps removing user from the DB

        :param uid: User ID
        :return True: If User deletion was successful,
            else an exception will be raised.
        """
        u_obj = User.get_by('id', uid)
        return u_obj.delete()

    @classmethod
    def get_existing_user_ids(cls,
                              uids: list,
                              get_objs: bool = False,
                              serialized: bool = False) -> list:
        """
        Takes list of user IDs and returns
        the records for those which are present in the DB

        :param uids: List of User IDs
        :param get_objs: If true user objects are returned
        :param serialized:
            get_objs flag must be set for this to work
            If this flag is set, serialized user data will be retuned
        """
        user_objs = User.get_existing_users(uids)
        if get_objs:
            if serialized:
                return UserSchema(many=True).dump(user_objs)
            return user_objs
        return [u.id for u in user_objs]

    @classmethod
    def list_roles(cls):
        return RoleSchema(many=True).dump(Role.list_roles())
