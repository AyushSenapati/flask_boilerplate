"""Module contains seed data for User management service
"""
import logging

# Application level imports
from app import db
from app.shared.exceptions.models import DBError
from .models import (User, Role)

logger = logging.getLogger(__name__)


def seed():
    """
    This function should be invoked when tables
    of user management service need be seeded
    """
    logger.info("Seeding Role...")
    for role in ['admin', 'sme', 'annotator']:
        r = Role(role)
        try:
            r.save_to_db()
            logger.debug(f"Role: {r.name} created.")
        except DBError:
            logger.error("possible reason - data already exists")
    logger.info("Seeding User...")
    u = User('John Smith', 'john@example.com', 'john@password', 1)
    try:
        u.save_to_db()
        logger.debug(f"Admin user: {u.email} with role: {u.role.name} created")
    except DBError:
        logger.error("possible reason - data already exists")
    logger.info('Setting up role hierarchy...')
    r_annon = db.session.query(Role).filter_by(name='annotator').first()
    r_sme = db.session.query(Role).filter_by(name='sme').first()
    r_admin = db.session.query(Role).filter_by(name='admin').first()
    r_annon.add_parent(r_sme)
    r_sme.add_parent(r_admin)
    r_admin.add_parent(r_admin)
    for role_obj in [r_annon, r_sme, r_admin]:
        db.session.add(role_obj)
    try:
        db.session.commit()
    except DBError:
        logger.error("possible reason - data already exists")
