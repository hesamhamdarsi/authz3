from functools import wraps

from flask import abort, request
from jwt import decode
from jwt.exceptions import ExpiredSignatureError

from authz.config import AuthConfig
from authz.model import Model_user

# here we should use database, and we should use role instead of username. but to simplify we used a dictionary
function_role_mapper = {
    "get_users": {"users": ["admin"]},  # if it was admin user, it can query all_users
    "get_user": {
        "users": [
            "admin",
            ":user_id",
        ]  # if it was admin user, or userx, it can see the userx information
    },
}


def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not request.is_json:
            abort(415)
        if "X-AUTH-Token" not in request.headers:
            abort(401)
        jwt_token = request.headers.get("X-AUTH-Token")
        try:
            jwt_token_data = decode(
                jwt_token, AuthConfig.JWT_SECRET, algorithms=[AuthConfig.JWT_ALG]
            )
        except ExpiredSignatureError:
            abort(401)
        except:
            abort(400)
        user = Model_user.query.get(jwt_token_data["user_id"])
        if user is None:
            abort(404)
        func_mapper = function_role_mapper[func.__name__]
        if user.username in func_mapper["users"]:
            return func(*args, **kwargs)
        elif ":user_id" in func_mapper["users"]:
            user_id_mapper = func.__code__.co_varnames.index("user_id")
            if args[user_id_mapper] == user.id:
                return func(*args, **kwargs)
            else:
                abort(403)
        else:
            abort(403)

    return wrapper
