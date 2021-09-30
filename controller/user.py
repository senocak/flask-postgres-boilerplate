from http import HTTPStatus
from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from model.user import UserResponse
from service import user_service
from util.exceptions import AppException
from util.helpers import json_response

user = Blueprint('user', __name__)


@user.route('/all', methods=['GET'])
@jwt_required()
def get_all():
    me = user_service.getUserById(get_jwt_identity()["identity"])
    try:
        get_all = user_service.get_all()
        data = UserResponse.UserSchema(many=True).dump(get_all)
        return json_response(data=data)
    except Exception as e:
        raise AppException(str(e), HTTPStatus.BAD_REQUEST.real)