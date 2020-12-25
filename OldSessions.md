# Session 10: 

### 1-flask-sqlalchemy 
in this section, we use flask-sqlalchemy as our ORM
we create a container for mysql with this envs:
```
MYSQL_ROOT_PASSWORD=<your_favorit_password>
MYSQL_DATABASE=authz   ---> name of database related to this service
MYSQL_USER=authz        ---> use service name as a the main user of database (best practice)
MSQ_PASSWORD=<Password belong to authz user>
```

##### Notice:
through sqlalchemy, we can change our backend database anytime we want for instance to postgres, we need to only change the connection stream in our code from mysql to postgres
Notice: using flask-sqlaalchemy, we will install sqlalchemy and also whatever needed for its integration with flask
any package like that which started with flask- has the same logic

---
### 2-wwwsqldesigner 
through wwwsqldesigner image, we willrun a container and design our mysql database
we save configuration using XML so it we need to do any change, like adding record, we use use that file
or if we wanted to restore that, we can use that file eithere 
```
docker run -d -p 8003:80 --rm --name sqld wwwsqldesigner
```
##### Notice:
in Microservices, we dont use "int" as primary_key. instead we use "varchar" for that. we call this "UUID". so the id feild of our user table and all other tables should be "varchar". why?
because when we are sending data from a service to another micro-service we may face problem. for instance, data is moved from a node which is big endian to another node which is little endian and so another user or container would be selected accidently 
this logic is called "endianness"

short explaintion: intel systems deal with data with little endian logic. in some other systems like ARM, system deal with data with big endian logic. this logic is difference between storing data in memory 
in little endian system, data with lower priority sits on a memory address which is lower, and data with higher priority sits on a memory address which is higher. in big endian its reversed

next we design our database and tables:

```
Table: user
  id = varchar64 (primary)
  username = varchar 128  (uniq and index)
  pass = varchar 128 
```
then we save XML forst, to have that as backup, we stor that in project->authz->docs

---
### 3-flask-marshmallow 
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
### 4-marshmallow-sqlalchemy 
installing marshmallow-sqlalchemy:
this package will provide integration between marshmallow and sqlalchemy. so we dont need to manually filter, serialize and de-serialize everything when its supposed to be written in sqlalchemy, instead marshmallow-sqlalchemy is doing that automatically for us

---
### 5-creating UUID liberary 
UUID definition/detection for entire project is the same. that means all microservices should use the same pattern. so when we want to write a code to generate UUID for us, we write it in shared section between the micro-services . project > Shared
this would be another code base 
after we've created our shared package, we need to make it installable to be installed on authz project
for that, we need to make a file called "setup.py" in "project > shared"
in this file we'll import a package called setuptools <and two modules in that(setup and find_packages)>

~/Downloads/programming/python/MS-test-2/shared$ cat shared/uuid.py 
```
from uuid import uuid4

def uuidgen():
    return uuid4().hex

```
 


~/Downloads/programming/python/MS-test-2/shared$ cat setup.py 
```
from setuptools import setup , find_packages

 setup(
        name="shared",
        version="1.0.0",
        description="shared liberary",
        author="hesam",
        author_email="myemail@example.com",
        packages=find_packages() #this will find all packages automatially
 )
```

lets come back to our previous env where we had our authz service. and then we move on to this directory and install our package through following:
```
(venv) hesam@HH-Host:~/Downloads/programming/python/MS-test-2/shared$ pip install .
Processing /home/hesam/Downloads/programming/python/MS-test-2/shared
Building wheels for collected packages: shared
  Building wheel for shared (setup.py) ... done
  Created wheel for shared: filename=shared-1.0.0-py3-none-any.whl size=1401 sha256=711d65ceeb7adc3219ceb699d46eb2ec5db9596321f1098232e2118223341259
  Stored in directory: /tmp/pip-ephem-wheel-cache-4wl373bs/wheels/83/bb/08/4f234c3f6b61bcbf34cb80beb8e3dfcaa145da0149afa79e98
Successfully built shared
Installing collected packages: shared
Successfully installed shared-1.0.0
```


as we installed this "shared" package, we can now import "uuidgen()" function from it
 
---
### 6-Installing Mysql 
```
docker container run -d -p 3308:3306 --name authz-mysql -e MYSQL_ROOT_PASSWORD=authz -e MYSQL_DATABASE=authz -e MYSQL_USER=authz -e MYSQL_PASSWORD=authz mysql:latest
```
and using wwwsqldesigner we design a new database (a table) for users
the XML output would be saved in project>docs>auth-sql.xml for later restoring in wwwsqldesiner

---
### 7-flask-migrate package
flask-migrate use to make our database ready through python codes. we need to install this package through "pip"
through this package, we can create automatic migrations to databases in python
we can simply get an mysql output from wwwsqldesigner, but this in not the right way. you need to use python to do that
we see how it works in the next lines

---
### 8-pymysql package
pymysql and pymysql[rsa] are packages(drivers) that we need to communicat with myswl. for other databases we need other packages
then we need to set ouu environment variable (connection stream to use mysql)
```
export AUTHZ_DATABASE_URL=mysql+pymysql://authz:authz@localhost:3306/authz
```
then we need to initial new migration 
```
flask db init
flask db migrate -m "Comment" 
flask db upgrade
```

test post: 
```
curl -i -H 'content-type: application/json' localhost:port/api/v1/users -d '{ "username": "hesam", "password": "123456" }'
```
---
### 9-marshmalo package extra description:
we make schema for user data (for both input and output)
for input, the reason is to prune mimselicious data, etc. 
for output the reason is to have more options over data. for example you want to say if data is password, do not send that to the user when you are getting all tables recored
```
password = mrmalo.auto_field(load_only=True)
```
so when client send a data like date/time, marshmallo will convert that to a data format in python, and when we want to send a data type like date/time from DB, ORM will get that and marshmalo convert that to a data with iso format standard and send that through JSON to client 

another example is when you have some daya types in database which is not supported by JSON to be pushed to client. like time/date, etc. for that you need to use marshmalo 

