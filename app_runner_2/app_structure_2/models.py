from .extensions import db


class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(21),nullable=False,unique=True)
    isVerified=db.Column(db.Boolean(),default=False)
    email=db.Column(db.String(128),nullable=False,unique=True)
    mobile_no=db.Column(db.String(10))
    role=db.Column(db.Integer,nullable=False)
    password=db.Column(db.String(128),nullable=False)