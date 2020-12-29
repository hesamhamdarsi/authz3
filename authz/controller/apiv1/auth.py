# begfore creating token, we need to get user/pass from user. if it was true we can create token
# for that we need to import user from Model to be able to check the user/pass
from time import time

# we need to be able to get the request(post), so we need to import that
from flask import abort, request
from jwt import decode, encode
from jwt.exceptions import ExpiredSignatureError

# to standardization, we need to read all configs (even custom configs) from the config file
# so anything that we need for jwt configuration, would be better to be defined there
from authz.config import AuthConfig
from authz.model import Model_user

# we also need to communicate through userschema(marshmalo)
from authz.schema.apiv1 import UsreSchema


class AuthController:
    def create_token():
        if not request.is_json:  # if request application-type was not JSON
            abort(415)
        user_schema = UsreSchema()
        data = user_schema.load(request.get_json())
        if (
            "username" in data and "password" in data
        ):  # check if request is sent correctly
            user = Model_user.query.filter_by(
                username=data["username"]
            ).first()  # check if user is in DB
            if user is None:
                abort(404)
            if user.password == data["password"]:
                current_time = time()
                jwt_token = encode(
                    {
                        "user_id": user.id,
                        "username": user.username,
                        "iss": "authz",
                        "iat": current_time,
                        "nbf": current_time,
                        "exp": current_time + AuthConfig.JWT_TOKEN_LIFETIME,
                    },
                    AuthConfig.JWT_SECRET,
                    algorithm=AuthConfig.JWT_ALG,
                )
                # return could be consists of 3 section, (data, status code and some headers)
                # header name for token could be anything, but here based on standard we call it X-Subject-Token
                return (
                    {"user": user_schema.dump(user)},
                    201,
                    {"X-Subject-Token": jwt_token},
                )
                pass
            else:
                abort(401)  # un-authorized
        else:
            abort(400)

    def verify_token():
        if not request.is_json:
            pass
        if "X-Subject-Token" not in request.headers:
            pass
        jwt_token = request.headers.get("X-Subject-Token")
        try:
            jwt_token_data = decode(
                jwt_token, AuthConfig.JWT_SECRET, algorithms=[AuthConfig.JWT_ALG]
            )
        # All exceptions: https://pyjwt.readthedocs.io/en/stable/api.html
        except ExpiredSignatureError:
            abort(401)
        except:
            abort(400)
        # in jwt_token = encode() section when we send a token to user, we embeded user_id as well. so user has it's own id now
        # when he send the token back, user_id should be embeded so. so through that, we can get user_id and check the user
        user = Model_user.query.get(jwt_token_data["user_id"])
        if user is None:
            abort(401)
        user_schema = UsreSchema()
        return {"user": user_schema.dump(user)}, 200, {"X-Subject-Token": jwt_token}
