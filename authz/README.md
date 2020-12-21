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