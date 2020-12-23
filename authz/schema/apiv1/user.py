from authz import mrmalo

from authz.model import Model_user

#here we could use mrmalo.Schema but then we need to manage all of our codes ourself 
#but we imported marshmallow-sqlalchemy to use that to do everything automated for us
class UsreSchema(mrmalo.SQLAlchemySchema):
 
    class Meta:
        #here we say what is our table (the class we made for this table in model section) or what are the fields
        #check the flask-marshmallow user manual
        model = Model_user     

    #id is filling automatically, so we need to say this field is dump_only and can only select that (not update)
    id = mrmalo.auto_field(dump_only=True)
    username = mrmalo.auto_field()
    #password shoud not be shown in return, so we spesify that as load_only. user cannot select that
    password = mrmalo.auto_field(load_only=True)

#we have to send this class to controller where we are writing to DB
