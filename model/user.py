from sqlalchemy import ForeignKey
from settings import db, fma
from marshmallow import Schema, fields, validate
from datetime import datetime
from werkzeug.security import check_password_hash
import uuid


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(60), primary_key=True, default=str(uuid.uuid4()))
    email = db.Column(db.String(60), index=True, unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=True)
    last_name = db.Column(db.String(250), nullable=True)
    address = db.Column(db.String(250), nullable=True)
    zip = db.Column(db.String(250), nullable=True)
    activated_at = db.Column(db.String(250), nullable=True)
    blocked_at = db.Column(db.String(250), nullable=True)
    roles = db.Column(db.JSON, default=['ROLE_USER'])
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, default=None)
    pass_reset = db.relationship('ResetPasswordRequest', backref='list', lazy=True)

    def __repr__(self):
        return '<Users {}>'.format(self.name)

    def checkPassword(self, password):
        return check_password_hash(self.password, password)


class ResetPasswordRequest(db.Model):
    __tablename__ = 'reset_password_request'
    id = db.Column(db.String(60), primary_key=True, default=str(uuid.uuid4()))
    selector = db.Column(db.String(60), nullable=True)
    hashed_token = db.Column(db.String(250), nullable=False)
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, default=None)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)


class UserRequest:
    class AuthSchema(Schema):
        email = fields.Email(required=True)
        password = fields.String(required=True, validate=[validate.Length(min=6, max=100)])
        remember_me = fields.Bool()

    class RegisterSchema(Schema):
        email = fields.Email(required=True)
        password = fields.String(required=True, validate=[validate.Length(min=6, max=100)])
        password_confirmation = fields.String(required=True, validate=[validate.Length(min=6, max=100)])
        name = fields.String(required=True, validate=[validate.Length(min=3, max=30)])
        last_name = fields.String(required=True, validate=[validate.Length(min=3, max=30)])
        address = fields.String(default=None)
        zip = fields.Integer(default=None)

    class PasswordResetRequestSchema(Schema):
        email = fields.Email(required=True)

    class PasswordResetSchema(PasswordResetRequestSchema):
        password = fields.String(required=True, validate=[validate.Length(min=6, max=100)])
        password_confirmation = fields.String(required=True, validate=[validate.Length(min=6, max=100)])


class UserResponse:
    class UserSchema(fma.Schema):
        class Meta:
            model = User
            fields = ('email', 'name', 'last_name', 'address', 'zip', 'activated_at', 'roles', 'blocked_at')
