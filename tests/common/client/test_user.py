# for controller > apiv1 > user.py
import pytest

# te test get_users function
#as we know for get_users() we need a token first, so we have to create a fake token
#for that, we need to first create a user
# as we are working on our test database, creating a test user is ok.
#notice: do not forget to lauch another mysql with a database called "testing" first, then changing database_uri to that DB before starting test

@pytest.mark.parametrize(
    ("headers", "json", "status"),
    [
        ({"Content-Type": "application/json"}, {"username":"admin" , "password":"admin"}, 201),
        ({"Content-Type": "application/json"}, {"user":"sss" , "passw":"sss"}, 403),
        ({"Content-Type": "application/json"}, {}, 403),
        ({"Content-Type": "application/json"}, {"username":"" , "password":""}, 405),
        ({"Content-Type": "application/json"}, {"username":"test" , "password":"test"}, 201),
        ({"Content-Type": "application/json"}, {"username":"test" , "password":"test"}, 409)
    ]
)

#here as we are trying to send a request, we need to use "user" fixture
def test_create_user(client, headers, json, status):
    result = client.post("api/v1/users", json=json, headers=headers)
    assert result.status_code == status

def test_get_users(client):
    token = client.post(
        "api/v1/auth/tokens",
        json={
            "username": "admin",
            "password":"admin"
        },
        headers={"Content-Type": "application/json"}
    )
    result = client.get(
        "api/v1/users",  
        headers={
            "X-AUTH-Token": token.headers["X-Subject-Token"],
            "Content-Type": "application/json"
        }
    )
    assert result.status_code == 200
    