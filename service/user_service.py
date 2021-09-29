from model.user import User
from util.exceptions import AppException


def get_all():
    return User.query.all()


def getUserById(_id):
    user = User.query.filter_by(id=_id).first()
    return user


def checkUserById(identity):
    user = getUserById(identity["id"])
    if user is None:
        raise AppException("Token and User not match")
    return user
