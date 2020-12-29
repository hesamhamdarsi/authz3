# __init__.py manual

```python
from flask import Flask, Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from authz.config import AuthConfig
```

blueprint is same as Flask from the code perspective. but the difference is blueprint can not be executed itself, so it should be registered by a Flask application because it needs WSGI server to run. that's why we need to register it in create_app() secion :

#### app.register_blueprint(bp_apiv1)

---
```python
bp_apiv1 = Blueprint("apiv1", __name__, url_prefix="/api/v1")
```

here are making a bluprint from Blueprint class (anything in python that import with capital Letter is a class).
each blueprint need at least a name (here apiv1) and a prefix that is blonged to this version

---
```python
# we can say db = SQLAlchemy(app), but as we didn't define our "app" yet, we should use "init_app" function to 
# import(initial) app in SQLAlchemy in create_app() section. this says which app should I initiate
db = SQLAlchemy()
mg = Migrate()
mrmalo = Marshmallow()

apiv1 = Api(bp_apiv1)  #creating apiv1

#this line can not be sent before apiv1 = Api(bp_apiv1), because in rosource we've imported apiv1
#that means if we import resource (below line), it has a line in it that say import apiv1 from this file
# as a result, first apiv1 should be defined in this file
# if we don't do this, we'll get "circular import" error
from authz import resource   


def create_app():
    app = Flask(__name__)
    app.config.from_object(AuthConfig)
    #we need to add configurations related to SQLAlchemy through config.py to be loaded to app 
    db.init_app(app)  
    mg.init_app(app, db)   
    mrmalo.init_app(app)              
    app.register_blueprint(bp_apiv1)
    return app
```

---
when we have our apiv2, we can simply make that using:
```
bp_apiv2 = Blueprint("apiv2", __name__, url_prefix="/api/v2")
apiv2 = Api(bp_apiv2)
```
and in create_app():
```
app.register_blueprint(bp_apiv2)
```
and then we need to make all required folders called apiv2 in al other parts of our other codes
this way, we don't need to remove anything from our code, if we wanted to switch our API we just simple commit the apiv1 in create_app() secion and use apiv2
```
# app.register_blueprint(bp_apiv1)
app.register_blueprint(bp_apiv2)
```

#### Serialization and deserialization:
Serialization means to convert an object into that string, and deserialization is its inverse operation. There are many third parties library that are “must have” libraries that are extremely popular and are often used in almost any android project

#### Flask-marshmallow:
https://flask-marshmallow.readthedocs.io/en/latest/
https://api-university.com/blog/rest-apis-with-hateoas/

---
### tesing backend services 
through the below config, we're going to add a command prompt for our application to help us to realize is every test before running the application passed

```python
from flask.cli import AppGroup
app_cli = AppGroup("app" , help= "Application related commands.")
def create_app():
    ...
    app.cli.add_command(app_cli)
    ...

```
using these codes, you'll see the command name(app) and description(Application related commands.) are added to flask.
```
flask --help
Commands:
  app     Application related commands.
  db      Perform database migrations.
  routes  Show the routes for the app.
  run     Run a development server.
  shell   Run a shell in the app context.
```
now we need to define our tests, for that we'll make another directory called "command" and its corresponding files and directories:
```
authz > authz > command > __init__.py
authz > authz > command > app > __init__.py
authz > authz > command > app > test.py
```

check the command > app > README.md