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
