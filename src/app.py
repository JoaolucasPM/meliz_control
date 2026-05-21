import os

from src.models.base import db, migrate
from flask_marshmallow import Marshmallow

from flask import Flask

ma = Marshmallow()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI = "sqlite:///project.db",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    from src.controllers.user import simple_user
    
    ma.init_app(app)
    
    db.init_app(app)
    
    migrate.init_app(app, db)
    app.register_blueprint(simple_user)
    
    return app