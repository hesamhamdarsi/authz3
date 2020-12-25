# decorator/apiv1/auth.py

```python
from functools import wraps
from flask import request, abort
from jwt import decode
from jwt.exceptions import ExpiredSignatureError

from authz.config import AuthConfig
from authz.model import Model_user

#here we should use database, and we should use role instead of username. but to simplify we used a dictionary
function_role_mapper = {
    "get_users": {
        "users": ["admin"]                 #if it was admin user, it can query all_users
    },
    "get_user": {
        "users": ["admin", ":user_id"]     #if it was admin user, or userx, it can see the userx information
    }
}

def auth_required(func):
    @wraps(func)
    def wrapper(*args , **kwargs):
        if not request.is_json:
            abort(415)
        if "X-AUTH-Token" not in request.headers:
            abort(401)
        jwt_token = request.headers.get("X-AUTH-Token")
        try:
            jwt_token_data = decode(
                jwt_token,
                AuthConfig.JWT_SECRET,
                algorithms=[AuthConfig.JWT_ALG]
            )
        except ExpiredSignatureError:
            abort(401)
        except:
            abort(400)
        user = Model_user.query.get(jwt_token_data["user_id"])
        if user is None:
            abort(404)
        func_mapper = function_role_mapper[func.__name__]
        if user.username in func_mapper["users"]:
            return func(*args , **kwargs)
        elif ":user_id" in func_mapper["users"]:
            user_id_mapper = func.__code__.co_varnames.index("user_id")
            if args[user_id_mapper] == user.id:
                return func(*args , **kwargs)
            else:
                abort(403)
        else:
            abort(403)
    return wrapper
```
### @Wrapss
Wraps is a decorator, that take a function and you can use that to get the name of that function or you can call any built-in function that is related to that function --> "dir(func)"
you could create auth_required without @wrapps, but then 
Wraps will get the function but then it the following line "func.__name__" would return "auth_required" instead of "get_user() and "get_users()" name:
func_mapper = function_role_mapper[func.__name__]
@Wraps always apply on Wrapper function, so you need to make Wrapper function for that

let's explain decorator and wraps simply in:
Authz > other references > decorator.md


---
Role based access control:
in reality, we need to make role for every user in DB and check that to auth people for certain resources. but here in this example we use a dictionary to spesify the users that have access to all user information or an spesific user information.
we want to say if a normal user want his information, he can grab it, but only admin user can get all users information and all spesific users information.
before that, we need to undestand some of the capablities of python:

let's create a simple function:
```
hesam@HH-Host:~$ python
Python 3.8.5 (default, Jul 28 2020, 12:59:40) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> def get_user(user_id):
...     return "test"
... 
```

lets test it
```
>>> get_user
<function get_user at 0x7f73a4f16670>
```

lets chack it's built-in functions:
```
>>> dir(get_user)
['__annotations__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
>>> 
```

we can detect the name of any function using:
```
>>> get_user.__name__
'get_user'
```

through code, we can check function argumants and indexs:
``` 
>>> get_user.__code__
<code object get_user at 0x7f73a4f1fb30, file "<stdin>", line 1>


>>> get_user.__code__.co_varnames
('user_id',)


>>> get_user.__code__.co_varnames.index("user_id")
0


>>> get_user.__code__.co_varnames[0]
'user_id'

```
__annotations__  will be used to add tags/lables to the function
__closure__      will be used to detect if our function is a closure function (has a parent function)


### fulle explaintion of all methods:
https://www.tutorialsteacher.com/python/magic-methods-in-python


#### so we use this capablities to return data that we want from the function. 
in function_role_mapper dictionary, we have two keys that their names are in fact functions name that we have in controller section
then through that, anywhere we need, we'll check if the user is an admin or a nomal user.
to do this we need to check which function we are calling:
```
func_mapper = function_role_mapper[func.__name__]
```
then we look in dictionary if username that we get is a part of users that should be or not. and so on
 
---
example for normal user to call get_users():
```
hesam@HH-Host:~$ curl -i -H 'Content-Type: application/json' -H 'X-AUTH-Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjoiNjFiNDI3N2NlOGI3NGVkYTgyYmU3MzRlN2VlMTc4M2QiLCJ1c2VybmFtZSI6Ikhlc2FtIiwiaXNzIjoiYXV0aHoiLCJpYXQiOjE2MDg3MzU3NjIuMTk0NTA5MywibmJmIjoxNjA4NzM1NzYyLjE5NDUwOTMsImV4cCI6MTYwODczNTg2Mi4xOTQ1MDkzfQ.4QoPETywryKGJ4YGwvlAGkg5Ce1W-shjXtOSpv2spvHzj7cTKR0Lh21OZEbHMTjT7P-8_wUtb7_ytzA846MHZg' 127.0.0.1:8081/api/v1/users
HTTP/1.0 403 FORBIDDEN
Content-Type: application/json
Content-Length: 144
Server: Werkzeug/1.0.1 Python/3.8.5
Date: Wed, 23 Dec 2020 15:03:08 GMT

{
    "message": "You don't have the permission to access the requested resource. It is either read-protected or not readable by the server."
}
```
---
example for normal user to call get_user() for its user_id:
```
hesam@HH-Host:~$ curl -i -H 'Content-Type: application/json' -H 'X-AUTH-Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjoiNjFiNDI3N2NlOGI3NGVkYTgyYmU3MzRlN2VlMTc4M2QiLCJ1c2VybmFtZSI6Ikhlc2FtIiwiaXNzIjoiYXV0aHoiLCJpYXQiOjE2MDg3MzU3NjIuMTk0NTA5MywibmJmIjoxNjA4NzM1NzYyLjE5NDUwOTMsImV4cCI6MTYwODczNTg2Mi4xOTQ1MDkzfQ.4QoPETywryKGJ4YGwvlAGkg5Ce1W-shjXtOSpv2spvHzj7cTKR0Lh21OZEbHMTjT7P-8_wUtb7_ytzA846MHZg' 127.0.0.1:8081/api/v1/users/61b4277ce8b74eda82be734e7ee1783d
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 74
Server: Werkzeug/1.0.1 Python/3.8.5
Date: Wed, 23 Dec 2020 15:03:49 GMT

{
    "username": "Hesam",
    "id": "61b4277ce8b74eda82be734e7ee1783d"
}
```
---
example for admin user (we should make a user called admin):
```
hesam@HH-Host:~$ curl -i -H 'Content-Type: application/json' -H 'X-AUTH-Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjoiMjY0N2E3NTg3NDFlNDRhY2E4MGE1Zjk0Mzk1YjIzY2IiLCJ1c2VybmFtZSI6ImFkbWluIiwiaXNzIjoiYXV0aHoiLCJpYXQiOjE2MDg3MzYwNzAuNTc0OTY5LCJuYmYiOjE2MDg3MzYwNzAuNTc0OTY5LCJleHAiOjE2MDg3MzYxNzAuNTc0OTY5fQ.GIXoQ7Jve2M3GjhxkTXfiFwspgKTjnCVaIzwY4V-qBMp7qXySI1-HNwIBgjEEHt19_2jr2RG1ITDmiUo2iJnOA' 127.0.0.1:8081/api/v1/users
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 644
Server: Werkzeug/1.0.1 Python/3.8.5
Date: Wed, 23 Dec 2020 15:08:25 GMT

[
    {
        "username": "heddsamww",
        "id": "0329e7055c474a1ca8889c21d75d18a1"
    },
    {
        "username": "hasan",
        "id": "0e590174ab9644ce9efa52f599093aca"
    },
    {
        "username": "admin",
        "id": "2647a758741e44aca80a5f94395b23cb"
    },
    {
        "username": "taleb",
        "id": "2fa907326bf84b1fad2a5dc66eddf714"
    }
    ....
]
```
