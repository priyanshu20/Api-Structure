from .extensions import api, bcrypt, jwt, limiter, db
from flask_restx import Resource
from .models import User
from flask import request
# from marshmallow import Schema, fields, validate
from flask_accepts import accepts, responds
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .utils import generate_otp, r
from .schemas import UserSchema, UserOutputSchema, OtpUserSchema, OtpVerificationSchema, LoginSchema, TestUserSchema
import datetime


'''
USER ROUTES
'''


user = api.namespace('user', description='Operations regarding user system')


@user.route('/signup')
class Signup(Resource):
    @accepts(schema=UserSchema, api=api)
    # @responds(schema=UserOutputSchema,api=api)
    def post(self):
        payload = request.json
        if User.query.filter_by(username=payload['username']).first() or User.query.filter_by(email=payload['email']).first() or User.query.filter_by(mobile_no=payload['mobile_no']).first():
            return {"message": "already exists"}
        else:
            hashed_pw = bcrypt.generate_password_hash(
                payload['password']).decode('utf-8')
            user_add = User(username=payload['username'], password=hashed_pw,
                            email=payload['email'], role=payload['role'], mobile_no=payload['mobile_no'])
            db.session.add(user_add)
            db.session.commit()
            return generate_otp(username=payload['username'], num=payload['mobile_no'])

    @responds(schema=UserOutputSchema(many=True), api=api, status_code=200)
    def get(self):
        users_found = User.query.all()
        return users_found


@user.route('/generateotp')
class Otp(Resource):
    @accepts(schema=OtpUserSchema, api=api)
    def post(self):
        payload = request.json
        user = User.query.filter_by(username=payload['username']).first()
        if user:
            if bcrypt.check_password_hash(user.password, payload['password']):
                if user.isVerified:
                    return {"message": "Your account is already verified"}
                else:
                    return generate_otp(username=user.username, num=user.mobile_no)
            else:
                return {"message": "wrong password"}
        else:
            return {"message": "user does not exist"}


@user.route('/verify')
class Verification(Resource):
    @accepts(schema=OtpVerificationSchema, api=api)
    @jwt_required
    def post(self):
        payload = request.json
        user = User.query.filter_by(username=get_jwt_identity()).first()
        if r.exists(user.username):
            if r.get(user.username) == payload['otp']:
                user.isVerified == True
                db.session.commit()
                return {"message": "Account verified!"}
            else:
                return {"message": "Wrong OTP"}
        else:
            return {"message": "Otp expired or does not exist"}


@user.route('/login')
class Login(Resource):
    @accepts(schema=LoginSchema, api=api)
    def post(self):
        payload = request.json
        user = User.query.filter_by(username=payload['username']).first()
        if user:
            if bcrypt.check_password_hash(user.password, payload['password']):
                expires = datetime.timedelta(minutes=30)
                token = create_access_token(
                    identity=payload['username'], expires_delta=expires)
                return {"message": "logged in!", "token": token}
            else:
                return {"message": "wrong password"}
        else:
            return {"message": "No such user"}
