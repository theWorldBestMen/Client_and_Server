from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from src.app import app, db

migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()
    
@manager.command
def drop_db():
    """Creates the db tables."""
    db.drop_all()


if __name__ == '__main__':
    manager.run()
