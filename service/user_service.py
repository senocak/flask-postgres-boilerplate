from model.user import User
from settings import db
from util.exceptions import AppException


def get_all():
    return User.query.all()


def getUserById(identity):
    user = User.query.filter_by(id=identity["id"]).first()
    if user is None:
        raise AppException("Token and User not match")
    return user


def getUserByEmail(email):
    return User.query.filter_by(email=email).first()


def create_user(data):
    user = User()
    for key in data:
        setattr(user, key, data[key])
    db.session.add(user)
    db.session.commit()
    return user
