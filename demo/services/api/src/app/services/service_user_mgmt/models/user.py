import logging
from passlib.hash import bcrypt
from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy.orm import validates
from marshmallow import fields, validate
from marshmallow_sqlalchemy import ModelSchema

# Application level import
from app import db, ma
from app.shared.exceptions.models import ResourceNotFound
from app.services.service_user_mgmt.models import Base, Role, RoleSchema

logger = logging.getLogger(__name__)


class User(Base):
    __tablename__ = 'users'

    id = db.Column(BIGINT, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    hashed_password = db.Column(db.String(100), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    role = db.relationship(
        'Role', backref=db.backref('user', lazy='dynamic')
    )

    def __init__(self, name, email, password, role_id):
        """
        :param str name: Name of the user
        :param str email: An unique email ID of the user
        :param str password: Raw password, which would be hashed before saving
        :param int role_id: A valid role id to be assigned to the user.
        """
        self.name = name
        self.email = email
        self.password = password
        self.role_id = role_id

    def __repr__(self):
        return "<{}(ID={}, email={})>".format(
            self.__class__.__name__, self.id, self.email
        )

    @validates('role_id')
    def validate_role_id(self, key, role_id):
        if role_id is None:
            return None
        # Check if Role with given role_id exists
        role = db.session.query(Role).get(role_id)
        if not role:
            raise ResourceNotFound(
                400, msg=f"Role ID:{role_id} not found."
            )
        return role.id

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = bcrypt.hash(password)

    def verify_password(self, password):
        """Verifies given password with stored hashed password

        :param str password: raw password to be matched with hashed password
        :return bool: True for correct and False for wrong password
        """
        return bcrypt.verify(password, self.hashed_password)

    @classmethod
    def list_users(cls, parsed_args):
        q = cls.get_base_query(parsed_args)
        q += cls.get_query_for_role(parsed_args.get('role_id'))
        q += cls.get_query_for_name(parsed_args.get('name'))
        q += cls.get_query_for_email(parsed_args.get('email'))
        return cls.get_result(q, parsed_args)

    @classmethod
    def get_query_for_role(cls, role_id):
        q = ''
        if role_id:
            q = f".filter_by(role_id={role_id})"
        return q

    @classmethod
    def get_query_for_name(cls, name):
        q = ''
        if name:
            q = f".filter_by(name='{name}')"
        return q

    @classmethod
    def get_query_for_email(cls, email):
        q = ''
        if email:
            q = f".filter_by(email='{email}')"
        return q

    @classmethod
    def get_user_by_email(cls, email):
        """Fetches User through email ID

        :param str email: Email ID of the User
        """
        u = db.session.query(cls).filter_by(email=email).first()
        if not u:
            raise ResourceNotFound(
                404, msg=f"User not found with email: {email}")
        return u

    @classmethod
    def get_by(cls, field, value):
        """Returns user object in case of no exception,
        else Resource not found custom exception will be raised
        """
        q = f'db.session.query({cls.__name__}).filter_by({field}={value}).first()'
        logger.debug(f"Generated Query: {q}")
        u = eval(q)
        if not u:
            raise ResourceNotFound(
                404, msg=f"User not found with {field}:{value}")
        return u

    @classmethod
    def get_existing_users(cls, uids):
        """Filters the DB with provided user
        ids and returns the IDs which are present

        :param list uids: List of User IDs
        :returns list: List of User IDs present in the DB
        """
        return db.session.query(cls)\
            .filter(cls.id.in_(uids))\
            .distinct().all()


class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
    role_id = fields.Integer(load_only=True)
    role = fields.Nested(RoleSchema, dump_only=True)

    class meta:
        ordered = True
