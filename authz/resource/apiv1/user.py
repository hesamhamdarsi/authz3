from flask_restx import Resource

from authz.controller.apiv1.user import User_Controller


class User_Resouce(Resource):
    def get(self, user_id=None):
        """
        Get user to get a user resource / Get users to get all user resources
        """
        if user_id == None:
            return User_Controller.get_users()
        else:
            return User_Controller.get_user(user_id)

    def post(self):
        """
        Create new user
        """
        return User_Controller.create_user()

    def patch(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
