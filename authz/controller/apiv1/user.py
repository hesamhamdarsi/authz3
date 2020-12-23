from authz import db
from flask import abort
from authz.model import Model_user
from flask import request      # we want to use POST, so we need to read requests coming from user
from authz.schema.apiv1 import UsreSchema
from authz.decorator.apiv1 import auth_required
class User_Controller:

    #maybe its query and not Query
    @auth_required
    def get_users():
        users = Model_user.query.all()
        #we want to use UserSchema, to check the validity of imformation that user ask for or send to us
        #many = true is because we have all users to check when we do "get users"
        users_schema = UsreSchema(many=True)
        return users_schema.dump(users)

    def get_user(user_id):
        user = Model_user.query.get(user_id)
        user_schema = UsreSchema()
        if user is None:
            abort(404)
        return user_schema.dump(user)
        
    def create_user():
        user_schema = UsreSchema()
        #POST will get some data from users. so we need to use request method and get those content as json
        data = user_schema.load(request.get_json())
        if "username" in data and "password" in data:
            #we need to check if "username" is in our database or not
            user = Model_user.query.filter_by(username=data["username"]).first()
            if user is None:
                user = Model_user(username = data["username"], password=data["password"])
                db.session.add(user)
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    abort(500)
                return user_schema.dump(user)
            else:
                abort(409)
        else:
            abort(400)