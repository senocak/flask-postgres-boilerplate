import functools
import os
from http import HTTPStatus
from flasgger import swag_from
from flask import jsonify, g
from flask_jwt_extended import get_jwt_identity
from flask_mail import Message

from service import user_service
from settings import mail
from util.constants import Roles
from util.exceptions import AppException


def json_response(success=True, messages=None, data=None, code=HTTPStatus.OK):
    if messages is None:
        messages = []

    if code not in [HTTPStatus.OK, HTTPStatus.CREATED]:
        success = False

    response = {
        'success': success,
        'code': code,
    }

    if len(messages):
        response.update({
            'messages': messages,
        })

    if data is not None:
        response.update({
            'data': data,
        })
    return jsonify(response), code


def doc(name, validation=False):
    return swag_from(os.path.join(os.getcwd(), 'swagger/{}.yaml'.format(name)), validation=validation)


def get_pagination_data(pagination):
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'prev': pagination.prev_num if pagination.prev_num > 0 else None,
        'next': pagination.next_num if pagination.next_num <= pagination.pages else None,
    }


def sendmail(subject, html, recipients):
    msg = Message(
        subject=subject,
        sender=(os.environ.get('MAIL_SENDER_NAME'), os.environ.get('MAIL_USERNAME')),
        recipients=recipients,
        html=html,
    )
    mail.send(msg)


def admin_role_required(func):
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        user = user_service.getUserById(get_jwt_identity())
        g.user = user
        if Roles.admin.value not in user.roles:
            raise AppException("User does not have valid role for this endpoint", HTTPStatus.UNAUTHORIZED.real)
        return func(*args, **kwargs)
    return new_func
