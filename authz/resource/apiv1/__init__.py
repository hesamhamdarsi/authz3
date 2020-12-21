from authz.resource.apiv1.user import User_Resouce
from authz.resource.apiv1.auth import AuthResource

from authz import apiv1 as api

api.add_resource(
    AuthResource,
    "/auth/tokens",
    methods=["GET","POST"],
    endpoint="auth_tokens"
)

api.add_resource(
    User_Resouce,
    "/users",
    endpoint="users"
)

api.add_resource(
    User_Resouce,
    "/users/<user_id>",
    endpoint="user"
    )