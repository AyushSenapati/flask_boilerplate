"""Module to manage the flask application"""
from flask.cli import FlaskGroup

# used to import modules dynamically
from importlib import import_module

from app import create_app, db
from app.services.service_user_mgmt.models import User, Role
from app.shared.exceptions.models import DBError

app = create_app()
cli = FlaskGroup(create_app=create_app)
logger = app.logger


# Custom cli commands goes here
@cli.command('recreate_db')
def recreate_db():
    logger.info('Dropping DB...')
    db.drop_all()
    db.create_all()
    logger.info('Recreating DB...')
    db.session.commit()
    logger.info('Done.')


@cli.command('seed')
def seed():
    # Check the installed services. If seed module is found under
    # that service, try to run the seed function of that seed module
    for service in app.config['INSTALLED_SERVICES'].keys():
        fqs_path = f"app.services.{service}"
        try:
            logger.info(f"Seeding service: {service}...")
            module = import_module('.seed', package=fqs_path)
            # Call the seed function of the particular service
            module.seed()
            logger.info(f"Seeding service: {service}... Done")
        except ImportError as e:
            logger.warning(
                f"Seeding service: {service}... Failed",
                extra={"reasons": f"Possible reason: [{e}]"}
            )


if __name__ == '__main__':
    cli()
