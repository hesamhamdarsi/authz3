# auth.py:


#### To test:
```
curl -i -H "content-type: application/json" 127.0.0.1:8081/api/v1/auth/tokens -d '{"username":"Hesam" , "password":"123456"}'
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 102
X-Subject-Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6Ikhlc2FtIiwiaXNzIjoiYXV0aHoiLCJpYXQiOjE2MDg1NTUxMDAuMTY2NTc1NCwibmJmIjoxNjA4NTU1MTAwLjE2NjU3NTQsImV4cCI6MTYwODU1NTIwMC4xNjY1NzU0fQ.TIl_kNBSExyECeoYoBZ15zgTrSPME2S6zWoOx2iK0qnvAfc0kxhU9t53jHkmRHFL6Ff01ilVD_ycnWTtRgXpuA
Server: Werkzeug/1.0.1 Python/3.8.5
Date: Mon, 21 Dec 2020 12:51:40 GMT

{
    "user": {
        "id": "61b4277ce8b74eda82be734e7ee1783d",
        "username": "Hesam"
    }
}
```

Notice: each token has 3 sections:
header.payload.signature
```
Header: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9
payload: eyJ1c2VybmFtZSI6Ikhlc2FtIiwiaXNzIjoiYXV0aHoiLCJpYXQiOjE2MDg1NTUxMDAuMTY2NTc1NCwibmJmIjoxNjA4NTU1MTAwLjE2NjU3NTQsImV4cCI6MTYwODU1NTIwMC4xNjY1NzU0fQ
signature: TIl_kNBSExyECeoYoBZ15zgTrSPME2S6zWoOx2iK0qnvAfc0kxhU9t53jHkmRHFL6Ff01ilVD_ycnWTtRgXpuA
```

if you use a week key, your token will be cracked very fast through some applications like "jwcat" and you key will be find
https://github.com/aress31/jwtcat


get_users():
we are using a decorator on this function, so whenever a get_users() is called, the client need to first send its auth_token. otherwise, he will be unauthorized 
check "README" on authz/decorator/apivi  