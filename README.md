# Session 11: 

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
### 2- auth file:

we are going to add a directory called decorator: Project > authz > authz > decorator

we are going to create "auth.py" file in the following directories:

Project > authz > authz > controller > apiv1

Project > authz > authz > resource > apiv1

