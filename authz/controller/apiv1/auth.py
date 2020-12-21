#begfore creating token, we need to get user/pass from user. if it was true we can create token
#for that we need to import user from Model to be able to check the user/pass
from authz.model import Model_user

from jwt import encode, decode
from time import time

#we also need to communicate through userschema(marshmalo)
from authz.schema.apiv1 import UsreSchema

#we need to be able to get the request(post), so we need to import that
from flask import request, abort

#to standardization, we need to read all configs (even custom configs) from the config file
#so anything that we need for jwt configuration, would be better to be defined there
from authz.config import AuthConfig

class AuthController:

    def create_token():
        if not request.is_json:   # if request application-type was not JSON
            abort(415)
        user_schema = UsreSchema()
        data = user_schema.load(request.get_json())
        if "username" in data and "password" in data:      #check if request is sent correctly
            user = Model_user.query.filter_by(username=data["username"]).first()  # check if user is in DB
            if user is None:
                abort(404)
            if user.password == data["password"]:
                current_time = time()
                jwt_token = encode(
                    {
                        "username": user.username,
                        "iss": "authz",
                        "iat": current_time,
                        "nbf": current_time,
                        "exp": current_time + AuthConfig.JWT_TOKEN_LIFETIME
                    },
                    AuthConfig.SECRET,
                    algorithm="HS512"
                )
                #return could be consists of 3 section, (data, status code and some headers)
                #header name could be anything, but here based on standard we call it X-Subject-Token
                return { "user": user_schema.dump(user) }, 201, {"X-Subject-Token": jwt_token}
                pass
            else:
                abort(401)  #un-authorized
        else:
            abort(400)

    def verify_token():
        pass
