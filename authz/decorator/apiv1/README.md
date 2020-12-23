```python
from functools import wraps
from flask import request, abort
from jwt import decode
from jwt.exceptions import ExpiredSignatureError

from authz.config import AuthConfig
from authz.model import Model_user
from authz.schema.apiv1 import UsreSchema

def auth_required():

    @wraps(func)
    def wrapper(*args , **kwargs):
        if not request.is_json:
            abort(415)
        if "X-AUTH-Token" not in request.json:
            abort(400)
        jwt_token = request.headers.get("X-AUTH-Token")
        try:
            jwt_token_data = decode(
                jwt_token,
                AuthConfig.JWT_SECRET,
                algorithms=AuthConfig.JWT_ALG
            )
        except ExpiredSignatureError:
            abort(401)
        except:
            abort(400)
        user_schema = user_schema()
        user = user_schema.query.get(jwt_token_data["user_id"])
        if user is None:
            abort(404)
        return func(*args , **kwargs)
    return wrapper
```
Wrap will get the function
Wrapper will take all or its argumants, and then Wrapper will be applied on that

then we apply this decorator on controller where we are calling get_users() or any other function which need auth

