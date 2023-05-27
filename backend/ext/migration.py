from flask_migrate import Migrate
from backend.ext.base import db

def init_app(app):
    migrate = Migrate()
    migrate.init_app(app, db)