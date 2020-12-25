### consider the following code:

```python
user = {"username": "jose", "access_level": "guest"}

def get_admin_password():
    return "1234"

print(get_admin_password()) 
```

we want to secure get_admin_password() in a way that if you call that somewhere in your program (like last line of code), only admin can execute it. consider you have this function or simillar to this function other places in your application as well.
one way to do that is just changing the code:
```python
def get_admin_password():
    if user["access_level"] == "admin":
        return "1234"
    else:
        return "None"
```

but its not a true method, as you have to manually change all of the simillar codes as well. so you use decorator to do that

```python
user = {"username": "jose", "access_level": "guest"}

def get_admin_password():
    return "1234"

def make_secure(func): 
    if user["access_level"] == "admin":
        return func()


get_admin_password = make_secure(get_admin_password)  # `get_admin_password` is now `secure_func` from above

print(get_admin_password()) 
```

as you see
1- we make another function (make_secure) before calling our main function (secure_function)
2- we send our main function as a argument in that function
3- inside that function, we make do our checks (or add functionality), and return the main function. So:
main function = deforator_func (main fucntion)


but this also has a problem, when access-level is admin, this will work correctly because it will check and so return the "func"
but when the user is not admin (e.g. guest), it will return "None". and None is not a function we are expecting as an output
so we need to change that by using another function inside the decorator, this function is what always return

```python
user = {"username": "jose", "access_level": "guest"}

def get_admin_password():
    return "1234"

def make_secure(func):
    def secure_function():
        if user["access_level"] == "admin":
            return func()

    return secure_function

get_admin_password = make_secure(get_admin_password)  # `get_admin_password` is now `secure_func` from above

print(get_admin_password()) 
```

#### so to make it more clear, we use the above code like:

```python
user = {"username": "jose", "access_level": "guest"}

def get_admin_password():
    return "1234"

def make_secure(func):
    def secure_function():
        if user["access_level"] == "admin":
            return func()

    return secure_function

@make_secure
get_admin_password

print(get_admin_password()) 
```

#### now we have another problem, as we know:
```
@make_secure
get_admin_password 
```
means:
```
get_admin_password = make_secure(get_admin_password)
and as we know we've used "return secure_function" inside our decorator. so that menas after our change:
get_admin_password = secure_function 
```
that means all biult-in functions will be change. for instance:
```python
get_admin_password.__name__ = secure function
```
we need to fix that, for that we use another decorator called @wraps which is a function in "functools" module.
this will keep the name and documentation of tha
it need to be on top of the inner function (secure_function). so we wrap the secure_func with func name,...:

```python
user = {"username": "jose", "access_level": "guest"}
from functools import wraps

def get_admin_password():
    return "1234"

def make_secure(func):
    @wraps(func)
    def secure_function():
        if user["access_level"] == "admin":
            return func()

    return secure_function

@make_secure
get_admin_password

print(get_admin_password()) 
```

#### now we have another problem:
how about our main function has some arguments and pointers? as we see, we don't pass them in secure_function and we don't return them in return func():
```
def secure_function():
        if user["access_level"] == "admin":
            return func()
```
to solve that we say get and retrn function with any number of args and pointers:

```python
user = {"username": "jose", "access_level": "guest"}
from functools import wraps

def get_admin_password():
    return "1234"

def make_secure(func):
    @wraps(func)
    def secure_function(*args, **kwargs):
        if user["access_level"] == "admin":
            return func(*args, **kwargs)

    return secure_function

@make_secure
get_admin_password

print(get_admin_password()) 
```

#### last change:
how about we have multiple different functions that should have different action. for instance, lets say we have two main functions:
get_admin_password()
get_my_password()

we need to take access_level as an arguments in our decortor to check that internally for different functions. so we need to make an extra layer of top of the decorator:

```python
user = {"username": "jose", "access_level": "guest"}
from functools import wraps

def get_admin_password():
    return "1234"

def extra_layer(access_level):
    def make_secure(func):
        @wraps(func)
        def secure_function(*args, **kwargs):
            if user[access_level] == "admin":
                DO_SOMTHING
                return func(*args, **kwargs)
            elif user[access_level] == "user":
                DO_SOMTHING
                return func(*args, **kwargs)
            else:
                DO_SOMTHING
                return func(*args, **kwargs)
        return secure_function
    return make_secure

@make_secure("admin")
get_admin_password

@make_secure("user")
get_my_password()
```