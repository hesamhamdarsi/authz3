from functools import wraps
from flask import request, abort
from jwt import decode
from jwt.exceptions import ExpiredSignatureError

from authz.config import AuthConfig
from authz.model import Model_user


def auth_required(func):
    @wraps(func)
    def wrapper(*args , **kwargs):
        if not request.is_json:
            abort(415)
        if "X-AUTH-Token" not in request.headers:
            abort(401)
        jwt_token = request.headers.get("X-AUTH-Token")
        try:
            jwt_token_data = decode(
                jwt_token,
                AuthConfig.JWT_SECRET,
                algorithms=[AuthConfig.JWT_ALG]
            )
        except ExpiredSignatureError:
            abort(401)
        except:
            abort(400)
        user = Model_user.query.get(jwt_token_data["user_id"])
        if user is None:
            abort(404)
        return func(*args , **kwargs)
    return wrapper
