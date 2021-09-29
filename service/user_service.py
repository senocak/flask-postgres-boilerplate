from model.user import User
from settings import db
from util.exceptions import AppException
from datetime import datetime


def get_all():
    return User.query.all()


def getUserById(_id):
    user = User.query.filter_by(id=_id).first()
    if user is None:
        raise AppException("User not found.")
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


def verify(user):
    user.activated_at = str(datetime.now())
    db.session.commit()
    return user
