from datetime import datetime
from http import HTTPStatus
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from model.user import UserRequest, UserResponse
from service import auth_service, user_service
from util.exceptions import AppException
from util.helpers import json_response, doc, admin_role_required

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
@doc('auth/login')
def login():
    request_data = UserRequest.AuthSchema().load(request.get_json())
    user = auth_service.login(request_data)
    data = auth_service.create_tokens(user.id, user.email, "remember_me" in request_data)
    return json_response(data=data)


@auth.route('/register', methods=['POST'])
@doc('auth/register')
def register():
    request_data = UserRequest.RegisterSchema().load(request.get_json())
    user = auth_service.register(request_data)
    #data = auth_service.create_tokens(user.id, user.email, False)
    return json_response(data="Please verify email", code=HTTPStatus.CREATED.real)


@auth.route('/resend/<email>', methods=['POST'])
@doc('auth/resend')
def resend(email):
    user = user_service.getUserByEmail(email)
    if user is None:
        raise AppException("User not found.", HTTPStatus.BAD_REQUEST.real)
    if user.activated_at is not None:
        raise AppException("User email is already verified", HTTPStatus.BAD_REQUEST.real)
    if user.blocked_at is not None:
        raise AppException("This user is blocked", HTTPStatus.BAD_REQUEST.real)

    auth_service.sendVerificationEmail(user)
    return json_response(data="Please check email")


@auth.route('/verify/<token>', methods=['POST'])
@doc('auth/verify')
def verify(token):
    user = user_service.getUserById(token)
    if user is None:
        raise AppException("User not found.", HTTPStatus.BAD_REQUEST.real)
    if user.activated_at is not None:
        raise AppException("User is already verified", HTTPStatus.BAD_REQUEST.real)
    if user.blocked_at is not None:
        raise AppException("User is blocked", HTTPStatus.BAD_REQUEST.real)
    user = user_service.verify(user)
    return json_response(messages="Your e-mail address has been verified. Thanks.")


@auth.route('/password', methods=['POST'])
@doc('auth/password')
def password():
    request_data = UserRequest.PasswordResetRequestSchema().load(request.get_json())
    user = user_service.getUserByEmail(request_data['email'])
    if user is None:
        raise AppException("User not found", HTTPStatus.BAD_REQUEST.real)
    if user.blocked_at is not None:
        raise AppException("User is blocked", HTTPStatus.BAD_REQUEST.real)
    pass_reset = user_service.getPassRequestsByUserId(user.id)
    if len(pass_reset) > 0:
        for ps in pass_reset:
            if ps is not None and datetime.now() < ps.expires_at:
                raise AppException("There is already a valid requested password reset request, please wait till max 1 "
                                   "day", HTTPStatus.BAD_REQUEST.real)
    pass_reset = user_service.create_pass_reset(user)
    auth_service.sendPassResetEmail(user, pass_reset)
    return json_response(data="Please check email")


@auth.route('/password/<token>', methods=['POST'])
@doc('auth/password-reset')
def password_reset(token):
    pass_reset = user_service.getPassRequestByHashedToken(token)
    if pass_reset is None:
        raise AppException("Password reset request not found", HTTPStatus.BAD_REQUEST.real)
    if datetime.now() > pass_reset.expires_at:
        raise AppException("Expired password reset request", HTTPStatus.BAD_REQUEST.real)
    request_data = UserRequest.PasswordResetSchema().load(request.get_json())
    if request_data["password"] != request_data["password_confirmation"]:
        raise AppException("Password and Confirmation are not matched", HTTPStatus.BAD_REQUEST.real)
    user_updated = user_service.updatePassword(request_data)
    return json_response(data="Password is updated.")


@auth.route('/me', methods=['GET'])
@doc('auth/me')
@jwt_required()
def me():
    me = user_service.getUserById(get_jwt_identity()["identity"])
    data = UserResponse.UserSchema().dump(me)
    return json_response(data=data)


@auth.route('/admin', methods=['GET'])
@jwt_required()
@admin_role_required
def admin():
    return json_response(data="Admin is here")


