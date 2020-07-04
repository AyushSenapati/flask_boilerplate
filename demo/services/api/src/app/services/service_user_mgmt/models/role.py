from marshmallow import fields

# Application level import
from app import db, ma
from app.services.service_user_mgmt.models import Base


roles_parents_mapping = db.Table(
    'roles_parents',
    Base.metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column(
        'child_role_id', db.Integer, db.ForeignKey('roles.id')),
    db.Column(
        'parent_role_id', db.Integer, db.ForeignKey('roles.id'))
)


class Role(Base):
    """Self joined Role model
    """
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    parents = db.relationship(
        'Role',
        remote_side=id,
        secondary=roles_parents_mapping,
        primaryjoin=(id == roles_parents_mapping.c.child_role_id),
        secondaryjoin=(id == roles_parents_mapping.c.parent_role_id),
        backref=db.backref('children', lazy='dynamic')
    )

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<{}(ID={}, name={})>".format(
            self.__class__.__name__, self.id, self.name
        )

    def add_parent(self, parent):
        # You don't need to add this role to parent's children set,
        # relationship between roles would do this work automatically
        self.parents.append(parent)

    @staticmethod
    def get_by_name(name):
        return db.session.query(Role).filter_by(name=name).first()

    @classmethod
    def list_roles(cls):
        return db.session.query(cls).all()


class RoleSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(dump_only=True)
