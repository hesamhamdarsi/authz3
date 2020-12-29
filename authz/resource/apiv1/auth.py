from flask_restx import Resource

from authz.controller.apiv1.auth import AuthController


class AuthResource(Resource):
    def get(self):
        """
        GET /auth/tokens  --> verify JWT token
        """
        return AuthController.verify_token()

    def post(self):
        """
        POST /auth/tokens  --> Create a new JWT token
        """
        return AuthController.create_token()
