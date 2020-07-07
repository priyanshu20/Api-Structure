from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db=SQLAlchemy()
api=Api()
bcrypt=Bcrypt()
jwt=JWTManager()
limiter=Limiter(key_func=get_remote_address,default_limits=["500 per day","50 per hour"])
