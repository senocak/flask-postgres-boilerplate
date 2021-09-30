import uuid
from werkzeug.security import generate_password_hash
from model.user import User, ResetPasswordRequest
from settings import db
from util.exceptions import AppException
from datetime import datetime, timedelta


def hashPassword(password):
    return generate_password_hash(password)


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


def create_pass_reset(user):
    pass_reset = ResetPasswordRequest()
    pass_reset.user_id = user.id
    pass_reset.selector = "selector"
    pass_reset.hashed_token = str(uuid.uuid4())
    pass_reset.expires_at = str(datetime.now() + timedelta(days=1))
    db.session.add(pass_reset)
    db.session.commit()
    return pass_reset


def getPassRequestsByUserId(_id):
    return ResetPasswordRequest.query.filter_by(user_id=_id).all()


def getPassRequestByHashedToken(_token):
    return ResetPasswordRequest.query.filter_by(hashed_token=_token).first()


def updatePassword(request_data):
    user = getUserByEmail(request_data["email"])
    user.password = hashPassword(request_data["password"])
    db.session.commit()
    return user
