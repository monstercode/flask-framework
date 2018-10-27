from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask_restful import abort

from api.models.user import UserModel


# https://media.readthedocs.org/pdf/flask-jwt-extended/latest/flask-jwt-extended.pdf


def has_any_role(roles=[]):
    def decorator(method):
        @wraps(method)
        def decorated_function(*args, **kwargs):
            user = get_jwt_identity()
            # intersect roles
            if len(list(set(roles) & set(user['roles']))) == 0:
                return abort(401)
           
            return method(*args, **kwargs)
        return decorated_function
    return decorator

def has_roles(roles=[]):
    def decorator(method):
        @wraps(method)
        def decorated_function(*args, **kwargs):
            user = get_jwt_identity()
            for role in roles:
                if role not in user['roles']:
                    return abort(401)
            return method(*args, **kwargs)
        return decorated_function
    return decorator

def has_role(role=None):
    def decorator(method):
        @wraps(method)
        def decorated_function(*args, **kwargs):
            user = get_jwt_identity()
            if role not in user['roles']:
                return abort(401)

            return method(*args, **kwargs)
        return decorated_function
    return decorator