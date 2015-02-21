# This file starts the WSGI web application.
# - Heroku starts gunicorn, which loads Procfile, which starts runserver.py
# - Developers can run it from the command line: python runserver.py

from app.app_and_db import app, db
from app.startup.init_app import init_app
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

init_app(app, db)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
# Start a development web server if executed from the command line
if __name__ == "__main__":
    manager.run()
