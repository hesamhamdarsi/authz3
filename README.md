# Session 11-12-13: 

### 1-pyjwt package
this package is for JWT token encode and decode 

you can test your jwt through https://jwt.io/ website

you can also check all liberaries of jwt for all programming language here in this site

we have a series of algorithms for encryption:
```
HS -> half security (e.g. HS256)
RS -> RSA
PS -> Primary Security
ES
```
some of hem need public/private key and some of them not

you can see all functions and classes of jwt using your terminal:
```
>>> import jwt
>>> dir(jwt)
['DecodeError', 'ExpiredSignature', 'ExpiredSignatureError', 'ImmatureSignatureError', 'InvalidAlgorithmError', 'InvalidAudience', 'InvalidAudienceError', 'InvalidIssuedAtError', 'InvalidIssuer', 'InvalidIssuerError', 'InvalidSignatureError', 'InvalidTokenError', 'MissingRequiredClaimError', 'PyJWS', 'PyJWT', 'PyJWTError', '__author__', '__builtins__', '__cached__', '__copyright__', '__doc__', '__file__', '__license__', '__loader__', '__name__', '__package__', '__path__', '__spec__', '__title__', '__version__', 'algorithms', 'api_jws', 'api_jwt', 'compat', 'decode', 'encode', 'exceptions', 'get_unverified_header', 'register_algorithm', 'unregister_algorithm', 'utils']

```
there are to main function so:
#### encode and decode
```
>>> jwt.encode({"username": "hesam"} , "123456")
b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Imhlc2FtIn0.zI_X9pISTvl8DG2SE7sfALdB2HjJWFrceHzr7xVdOEY'

>>> jwt.decode("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Imhlc2FtIn0.zI_X9pISTvl8DG2SE7sfALdB2HjJWFrceHzr7xVdOEY" , "123456")
{'username': 'hesam'}

>>> jwt.decode("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Imhlc2FtIn0.zI_X9pISTvl8DG2SE7sfALdB2HjJWFrceHzr7xVdOEY" , "wrong-key")
Traceback (most recent call last):....
jwt.exceptions.InvalidSignatureError: Signature verification failed

```

example of setting other variables:
```
>>> jwt.encode({"username": "hesam", "exp": time.time()+25, "nbf": time.time(), "iat": time.time()} , "123456", algorithm="HS512")
b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZS...IlK2fQs_kM8Bme-1SWaCY'
```
#### Notice: 
b'.....' -> b=binary. so when you want to send it to client, you need to convert it to utf-8. so:
```
>>> jwt.encode({"username": "hesam", "exp": time.time()+25, "nbf": time.time(), "iat": time.time()} , "123456", algorithm="HS512").decode("utf8)
'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZS...IlK2fQs_kM8Bme-1SWaCY'
```

Now using decode, we can authorise it
```
>>> jwt.decode("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZS...IlK2fQs_kM8Bme-1SWaCY" , "123456")
{'username': 'hesam', 'exp': 1608533566.216692, 'nbf': 1608533541.2166934, 'iat': 1608533541.2166934}

After 25 Second: 
>>> jwt.decode("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZS...IlK2fQs_kM8Bme-1SWaCY" , "123456")
...
raise ExpiredSignatureError('Signature has expired')
jwt.exceptions.ExpiredSignatureError: Signature has expired

```
So the Idea behind this is when a client/user get this token, it can talk with all services through this token and as far as all micriservices have the key, they can open this token and verify it. 

---
### 2-auth file:

we are going to create "auth.py" file in the following directories:

Project > authz > authz > controller > apiv1

Project > authz > authz > resource > apiv1

---
### 3-Decorator:

we are going to add a directory called decorator: Project > authz > authz > decorator
through decorator, we can specify authentication from some resources. for instance, normal users shouldn't be able to see the list of all users
why we should use decorator? because we want if anyone called get_users() function, frist have to be authenticated, but we don't want this to be done by changing in get_users() function. we need to devorate get_users() functions and add some capabilities to it (auth check). 

---
### 4- Test application backing services and dependencies:
we'll add the following directorie and files:
authz > authz > command > app > test.py
authz > start.py
#### notice: we better ti use bash script, so there is another file here to do the same test using bash script:
authz > start.sh
1-chech authz> __init__.py manual page
2- authz > command > app > README.md

---
### 5-Containerize the project:
steps:
5-1-Creating Dockerfile in authz >
5-2-creating .dockerignore file to prevent to ship all files inside our directory. for instance, we don't want to send venv directory and so on. 
the content of this file is exactly like .gitignore and we also add .gitignore in this file (we need to add .dockerignore in .gitignore file later on)
you can check Dockerfile
5-3- in production, we don't use "flask run" and instead we use another WSGI server called "gunicorn"
```
pip install gunicorn
```
now in order to run our application we can use;
```
gunicorn -b 0.0.0.0:8005 -w 6 --threads 3 --access-logfile - --error-logfile - --log-level - "authz:create_app()"
```
if we start to build Dockerfile, we'll get an error for shared package, becuase in Dockerfile, the path for shared package which is a local package is not clear.
to solve that, we need to first create an image from Shared and build that, and then build our main app from that image.
chech the Dockerfile in shared folder 

After that, we should remove shared package from our main app requirements.txt file because it will be imported through the shared image
```
pip uninstall shared
```

---
### 6-Unit test
manual at authz > tests > README.md


---
#### Notice:
you need to write your codes based on pep8 style guid standard:
https://www.python.org/dev/peps/pep-0008/

there are 3 packages that help you out for that:
isort: sort all imports that we have in our codes
flake8: will return the lines that have standard problem in our codes
black: will fix all these items
```
pip install isort flake8 black
flake8 authz/
isort authz/
black authz/
```