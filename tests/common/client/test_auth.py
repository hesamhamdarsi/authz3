#for decorator > apiv1 > auth.py
import pytest

# through patametrize, we'll define a "tupple" including items for send and recive, 
# and we'll define a "list" including data that we want to send nd result that we expect as recieve 
@pytest.mark.parametrize(
    ("headers", "status"),
    [
        ({}, 415),
        ({"Content-Type" : "application/json"}, 401),
        ({"Content-Type" : "application/json" , "X-AUTH-Token" : "null"}, 401)
    ]
)

#as we want to send a request, we need to load client fixture
#his client need a request and expected response, so we call them from "@pytest.mark.parametrize"
def test_auth(client, headers, status):
    result = client.get("api/v1/users", headers=headers)
    assert result.status_code == status