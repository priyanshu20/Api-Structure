from flask import Flask
from .extensions import db,api,bcrypt,jwt,limiter
from .user_views import user

def create_app(config_file='config.py'):
    app=Flask(__name__)
    app.config.from_pyfile(config_file)

    db.init_app(app)
    api.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    with app.app_context():
        db.create_all()
        


        return app
