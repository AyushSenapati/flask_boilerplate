"""Module to manage the flask application"""

from flask.cli import FlaskGroup

from app import create_app, db

app = create_app()
cli = FlaskGroup(create_app=create_app)

# Custom cli commands goes here
@cli.command('recreate_db')
def recreate_db():
    print('Dropping DB...')
    db.drop_all()
    db.create_all()
    print('Recreating DB...')
    db.session.commit()
    print('Done.')


if __name__ == '__main__':
    cli()
