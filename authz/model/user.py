from shared import uuidgen
from authz import db

#here in model we just create our database. if we want to grap any data, insert any,... 
#we'll use controller. so we need to import db in controller as well, because we neded to create session with database there
#db.Model is the schema that we designed(DB) before(we need to design our DB before writing codes)
#for each table we need to make a seperate class.and class name that you use will be converted to table in Database
#so when you define Model_user, a table in database will be created named "Model_user"
#if you need to use another nale rather that class_name you can set this value in block:
#class User(db.Model):
#    ____tablename____ = "my_user_table"
class Model_user(db.Model): 

    #For ID we need to generate UUID for user to put that in Default value 
    id = db.Column(db.String(64), primary_key = True, default=uuidgen)
    username = db.Column(db.String(128), unique = True, index = True, nullable = False)
    password = db.Column(db.String(128), nullable = False)

