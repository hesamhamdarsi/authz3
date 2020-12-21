# user.py manual

```python
from authz import mrmalo

from authz.model import Model_user

#here we could use mrmalo.Schema but then we need to manage all of our codes ourself 
#but we imported marshmallow-sqlalchemy to use that to do everything automated for us
class UsreSchema(mrmalo.SQLAlchemySchema):
    class Meta:
        model = Model_user     #here we say what is our table (the class we made for this table in model section)

    #id is filling automatically, so we need to say this field is dump_only
    id = mrmalo.auto_field(dump_only=True)
    username = mrmalo.auto_field()
    #password shoud not be shown in return, so we spesify that as load_only
    password = mrmalo.auto_field(load_only=True)

#we have to send this class to controller where we are writing to DB
```
### flask-marshmallow 
installing flask-marshmallow:
when data wanted to be exchange between Model and database, we need to apply some filters to prevemt users from injecting bad data in database (ind of security)
we should initiate that in create_app section as well:
```
mrmalo = Marshmallow()
create_app():
   ...
   mrmalo.init_app(app) 
   ...
```
---
### marshmallow-sqlalchemy 
installing marshmallow-sqlalchemy:
this package will provide integration between marshmallow and sqlalchemy. so we dont need to manually filter, serialize and de-serialize everything when its supposed to be written in sqlalchemy, instead marshmallow-sqlalchemy is doing that automatically for us

---
### marshmalo package extra description:
we make schema for user data (for both input and output)
for input, the reason is to prune mimselicious data, etc. 
for output the reason is to have more options over data. for example you want to say if data is password, do not send that to the user when you are getting all tables recored
```
password = mrmalo.auto_field(load_only=True)
```
so when client send a data like date/time, marshmallo will convert that to a data format in python, and when we want to send a data type like date/time from DB, ORM will get that and marshmalo convert that to a data with iso format standard and send that through JSON to client 

another example is when you have some daya types in database which is not supported by JSON to be pushed to client. like time/date, etc. for that you need to use marshmalo 