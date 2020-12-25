from flask import Flask, Blueprint
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask.cli import AppGroup
from authz.config import AuthConfig

bp_apiv1 = Blueprint("apiv1", __name__, url_prefix="/api/v1")

#we can say db = SQLAlchemy(app), but as we didn't define our "app" yet, we should use "init_app" function to 
# import app in SQLAlchemy in create_app() section. this says which app should I initiate
db = SQLAlchemy()
mg = Migrate()
mrmalo = Marshmallow()

apiv1 = Api(bp_apiv1)
app_cli = AppGroup("app" , help= "Application related commands.")

#this line can not be sent before apiv1 = Api(bp_apiv1), because in rosource we've imported apiv1
#that means if we import resource (below line), it has a line in it that say import apiv1 from this file
# as a result, first apiv1 should be defined in this file
from authz import resource

#we want to have command prompt for "app -> test.py" defined in command folder. so it should be loaded in main application (this file)
from authz import command   

def create_app():
    app = Flask(__name__)
    app.config.from_object(AuthConfig)
    #we need to add configurations related to SQLAlchemy through config.py to be loaded to app 
    db.init_app(app)  
    mg.init_app(app, db)   
    mrmalo.init_app(app)              
    app.register_blueprint(bp_apiv1)
    app.cli.add_command(app_cli)
    return app
