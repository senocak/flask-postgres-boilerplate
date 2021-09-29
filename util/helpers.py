import os
from http import HTTPStatus
from flasgger import swag_from
from flask import jsonify


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
