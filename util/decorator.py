import functools
from flask import g
from flask_jwt_extended import get_jwt_identity
from service import user_service


def check_roles_for_admin(func):
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        identity = get_jwt_identity()
        user = user_service.getUserById(identity["id"])
        g.user = user
        """
        if Roles.admin.value not in user.roles:
            raise UserRolesPermission
        else:
            return func(*args, **kwargs)
        """
        return func(*args, **kwargs)
    return new_func
