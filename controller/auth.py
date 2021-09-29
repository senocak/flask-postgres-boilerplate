from http import HTTPStatus
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from model.user import Request, Response
from service import auth_service, user_service
from util.exceptions import AppException
from util.helpers import json_response, doc, admin_role_required

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
@doc('auth/login')
def login():
    request_data = Request.AuthSchema().load(request.get_json())
    user = auth_service.login(request_data)
    data = auth_service.create_tokens(user.id, user.email, "remember_me" in request_data)
    return json_response(data=data)


@auth.route('/register', methods=['POST'])
@doc('auth/register')
def register():
    request_data = Request.RegisterSchema().load(request.get_json())
    user = auth_service.register(request_data)
    data = auth_service.create_tokens(user.id, user.email, False)
    return json_response(data=data, code=HTTPStatus.CREATED.real)


@auth.route('/verify/<token>', methods=['POST'])
@doc('auth/verify')
def verify(token):
    user = user_service.getUserById(token)
    if user.activated_at is not None:
        raise AppException("User is already verified", HTTPStatus.BAD_REQUEST.real)
    if user.blocked_at is not None:
        raise AppException("User is blocked", HTTPStatus.BAD_REQUEST.real)
    user = user_service.verify(user)
    return json_response(messages=["Your e-mail address has been verified. Thanks."])


@auth.route('/me', methods=['GET'])
@doc('auth/me')
@jwt_required()
#@admin_role_required
def me():
    me = user_service.getUserById(get_jwt_identity()["identity"])
    data = Response.UserSchema().dump(me)
    return json_response(data=data)

