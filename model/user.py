from settings import db, fma
from marshmallow import Schema, fields, validate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.String(60), primary_key=True, autoincrement=True)
    email = db.Column(db.String(60), index=True, unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=True)
    last_name = db.Column(db.String(250), nullable=True)
    address = db.Column(db.String(250), nullable=True)
    zip = db.Column(db.String(250), nullable=True)
    activated_at = db.Column(db.String(250), nullable=True, unique=True)
    blocked_at = db.Column(db.String(250), nullable=True, unique=True)
    roles = db.Column(db.String(250), default=['USER'])
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Users {}>'.format(self.name)

    def setPassword(self, password):
        self.password = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password, password)


class Request:
    class AuthSchema(Schema):
        email = fields.Email(required=True)
        password = fields.String(required=True, validate=[
            validate.Length(min=6, max=100)
        ])
        remember_me = fields.Bool()


class Response:
    class UserSchema(fma.Schema):
        class Meta:
            model = User
            fields = ('email', 'name', 'last_name', 'address', 'zip', 'activated_at', 'roles', 'blocked_at')
