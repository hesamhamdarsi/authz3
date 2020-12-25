#### context manager and ocntext manager syntax(with):
https://virgool.io/@GreatBahram/once-for-ever-context-manager-qqqbqxgryxk5

#### Request context vs application context:
the idea of speaking about this subject is handling requests or some jobs that are time consuming in the background to do not make your code pause until the job is finished, like connecting and doing something on DB, sending Email, etc
we should pass this job to another thread. but python has dependency to the thread that original request/application was in. if you send this job/request to another thread, it wont work until you have the exact copy of request and also your application context available there.
good explaintion here:

https://blog.miguelgrinberg.com/post/flask-webcast-2-request-and-application-contexts
or here:
https://www.youtube.com/watch?v=Z4X5Oddhcc8&feature=youtu.be

when our flask application come up, there are two context that are created by flask:
application context and request context

#### All of the following items need a valid or fake request:
Request object is associated with request variable(what client send in web request)
Session object is associated with session cookie in the request (inside the client request)
current_user is assiciated with auth information or the session cookie that come with request

otherwise, you will get an error:
```
Working outside of request context
```
#### Application context:
when you run your application, flask will create an application context, and then will put the application instance in it
Current_app object links to this application instance which is stored in application context
also there is another object called "g" which is linked to application context and there is no dependecy to the request context
```
from flask import current_app
from app_directory import my_app
```
the above code, will create an applicatin context and install that in a thread
now, if I say:
```
with my_app.app_context():
    print(current_app.config)
```
it will load the configs related to that application.
another method of creating this context is:
```
from flask import current_app
from app_directory import my_app

ctx = my_app.app_context()

ctx.push()  #when we start
current_app.config

ctx.pop()   #when we're done
```