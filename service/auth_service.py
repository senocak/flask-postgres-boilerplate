from http import HTTPStatus
from model.user import User
from settings import db
from flask import request, jsonify
from flask_jwt_extended import *
from util.exceptions import AppException
from util.helpers import json_response


def login(request_data):
    res = {}
    try:
        email = request_data['email']
        password = request_data['password']
        user = User.query.filter_by(email=email).first()

        if not user:
            res['msg'] = "User not registered !"
            return json_response(res, 400)

        if not user.checkPassword(password):
            res['msg'] = "Email/Password"
            return json_response(res, 400)

        data = {'id': user.id, 'email': user.email}

        res['access_token'] = create_access_token(identity=data, fresh=True)
        if "remember_me" in request_data:
            res['refresh_token'] = create_refresh_token(identity=data)
        return res
    except Exception as e:
        raise AppException(str(e), HTTPStatus.BAD_REQUEST.real)


def saveSuperAdmin():
    res = {}
    try:
        full_name = request.form.get('full_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        data = [{
            'username': username,
            'email': email,
        }]

        user = User(full_name=full_name, username=username, email=email)
        user.setPassword(password)
        db.session.add(user)
        db.session.commit()

        res['data'] = data
        res['msg'] = "Data added successfully !"
        return json_response(res)
    except Exception as e:
        raise AppException(str(e), HTTPStatus.BAD_REQUEST.real)
