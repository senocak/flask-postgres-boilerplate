import os
from http import HTTPStatus
from flask import render_template
from werkzeug.security import generate_password_hash
from service import user_service
from flask_jwt_extended import *
from util.exceptions import AppException
from util.helpers import sendmail


def create_tokens(_id, email, remember_me):
    res = {}
    data = {'id': _id, 'email': email}
    res['access_token'] = create_access_token(identity=data, fresh=True)
    if remember_me is True:
        res['refresh_token'] = create_refresh_token(identity=data)
    return res


def login(request_data):
    email = request_data['email']
    password = request_data['password']
    user = user_service.getUserByEmail(email)
    if user is None:
        raise AppException("There is no any user with this email", HTTPStatus.UNAUTHORIZED.real)
    if not user.checkPassword(password):
        raise AppException("Email and Password do not match", HTTPStatus.UNAUTHORIZED.real)
    if user.blocked_at is not None:
        raise AppException("User is blocked", HTTPStatus.UNAUTHORIZED.real)
    if user.activated_at is None:
        raise AppException("User must be activated for auth", HTTPStatus.UNAUTHORIZED.real)
    return user


def register(request_data):
    user = user_service.getUserByEmail(request_data['email'])
    if user is not None:
        raise AppException("There is already a user with this email", HTTPStatus.BAD_REQUEST.real)

    if request_data['password'] != request_data['password_confirmation']:
        raise AppException("Password not matched", HTTPStatus.BAD_REQUEST.real)

    data = {
        'email': request_data['email'],
        'name': request_data['name'],
        'last_name': request_data['last_name'],
        "password": user_service.hashPassword(request_data['password']),
        'address': request_data['address'] if "address" in request_data else None,
        'zip': request_data['zip'] if "zip" in request_data else None
    }
    user = user_service.create_user(data)
    sendVerificationEmail(user)
    return user


def sendVerificationEmail(user):
    subject = 'User Verification Email'
    sendmail(
        subject=subject,
        html=render_template('mail/user_register_verification.html',
                             subject=subject,
                             url='{}/kullanici-onay/{}'.format(os.environ.get('FRONTEND_URL'), user.id)),
        recipients=[user.email]
    )


def sendPassResetEmail(user, pass_reset):
    subject = 'Password Reset Email'
    sendmail(
        subject=subject,
        html=render_template('mail/user_pass_reset.html',
                             subject=subject,
                             url='{}/pass-reset/{}'.format(os.environ.get('FRONTEND_URL'), pass_reset.hashed_token)),
        recipients=[user.email]
    )
