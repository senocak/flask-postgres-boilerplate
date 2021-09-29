from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from model.user import Request, Response
from service import auth_service, user_service
from util.exceptions import AppException
from util.helpers import json_response, doc

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
@doc('auth/login')
def login():
    request_data = Request.AuthSchema().load(request.get_json())
    data = {"token": auth_service.login(request_data)}
    return json_response(data=data)


@auth.route('/me', methods=['GET'])
@doc('auth/me')
@jwt_required()
def me():
    me = checkUserById(get_jwt_identity())
    data = Response.UserSchema().dump(me)
    return json_response(data=data)


#@jwt.expired_token_loader

def checkUserById(identity):
    user = user_service.getUserById(identity["id"])
    if user is None:
        raise AppException("Token and User not match")
    return user
