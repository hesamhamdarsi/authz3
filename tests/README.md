## Unit test:
first we need the following packages to be installed:
```
Pytest : test the application
Coverage: how much thee tests through pytest can cover my code
```

### creating a directory for all of our tests:
Authz > tests 

#### we have normally for section to test our applications. we're going to make a directory for each one:

#### 1-Common: 
Unit test is used for small code blocks (functions)
```
Inside here we could have 3 different test categories:
Start:
- All warm up tests that we need will be placed here
Client:
- All blocks and functions that are related to different functions 
runner:
?
```
#### 2-Security:
used to check all security parameters

#### 3-Integration:
here we test The entire microservice
Performance evaluating 
Using different backing service like postgres, mysql, etc
Checking internal communications (like when a part is sending a request to another part)

#### 4-Functional:
All microservices are up and the entire application would be tested

---
#### we have the following files inside 
Authz > test > conftest.py   → test configuration

```python
import pytest
from authz import create_app

#the following items are mandetory in all projects
#creating an instance of application
@pytest.fixture
def app():
    app = create_app()
    return app

#creating a test_client and help us to without running flask (flask run) we send request to the endpoints and get back the result
@pytest.fixture
def client(app):
    return app.test_client()

#help us to immplement command prompt that we've created before(e.g. flask app test)
@pytest.fixture
def runner(app):
    return app.test_cli_runner()
```
fixtures are the primary configurations that you need to test every function
There is a service in Flask called “test_client” that will help you to do not need to make context and current_app for your unit test

running “conftest.py” return an error on this line:
```
From authz import create_app().
```
For this, we need to create 2 other files in Auth > 
pytest.ini     ---> to specify the test paths (here tests)
.coveragerc   → to specify the test package (here authz)

#### .converagerc file:
```
[run]
source = authz
branch = True
```
In coverage we need to specify the project path, otherwise, we'll have the above error
```
Command : coverage run -m pytest
```
This command will inject all tests that we’ve created in “tests” directory. and also all fixtures that we made in conftest.py, will be injected as well. The second part helps us to do not have to import packages in our test files  

#### Notice on unit tests (common section): 
all test files that we will create should be based on this template:
```
test_name.py   or   name_test.py
```
All functions inside these files should follow the same standard:
```
test_func_name()    or    func_name_test()
```

for functional test and integration tests the rules are different

#### For example for unit test:
We’ll make a warmup test to check ENV and database name
We’ll make a client test to test all functions of the “auth.py”  --->  authz > authz > decorator > apiv1 > auth.py

After creating all of these files we use this command to see the output of tests:
```
overage run -m pytest
```

Also we can use the following command to make an html page including the percentage of covering all tests:
```
coverage html
```

Output will be an index.html and you can find it through authz > htmlcov > index.html
You will see all of your packages and other packages you used in your application and you can check if each package passed at least 90%

#### Notice:
before running test, change your database and AUTHZ_DATABASE_URI to "testing" database
```
docker container run -d -p 3308:3306 --name authz-test-mysql -e MYSQL_ROOT_PASSWORD=authz -e MYSQL_DATABASE=testing -e MYSQL_USER=authz -e MYSQL_PASSWORD=test mysql:latest

export AUTHZ_DATABASE_URL=mysql+pymysql://authz:authz@localhost:3308/testing
```
