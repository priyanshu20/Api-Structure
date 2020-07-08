from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    username = fields.String(
        required=True, validate=validate.Length(min=3, max=20))
    email = fields.Email(required=True)
    password = fields.String(
        required=True, validate=validate.Length(min=3, max=20))
    role = fields.Int(
        required=True, validate=validate.OneOf(choices=[1, 2]))
    mobile_no = fields.String(
        required=True, validate=validate.Regexp(regex='^[6-9]\d{9}$'))


class UserOutputSchema(Schema):
    username = fields.String()
    role = fields.Int()
    isVerified = fields.Bool()


class OtpUserSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)


class OtpVerificationSchema(Schema):
    otp = fields.Int(required=True, validate=validate.Range(
        min=100000, max=999999))
    token = fields.String(required=True)


class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)


class TestUserSchema(Schema):
    username = fields.String(required=False)
    mobile_no = fields.String(required=False)
    token = fields.String(required=True)
