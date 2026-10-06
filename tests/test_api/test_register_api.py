from playwright.sync_api import expect
from pages.pages_api.client_user import ClientUser
from test_data.user_api import make_user_body,UserMissingField,UserBrokenBody
import pytest

@pytest.mark.api
@pytest.mark.smoke
def test_CreateUser(api_client):
    UserBody = make_user_body()
    FirstName = UserBody["firstName"]
    LastName = UserBody["lastName"]
    UserName = UserBody["username"]

    ApiClient = ClientUser(api_client)
    Response = ApiClient.CreateUser(UserBody)
    expect(Response).to_be_ok()
    assert Response.status == 201
    assert Response.status_text == "Created"
    ResponseBody = Response.json()
    assert "id" in ResponseBody["user"]
    assert "uuid" in ResponseBody["user"]
    assert FirstName == ResponseBody["user"]["firstName"]
    assert LastName == ResponseBody["user"]["lastName"]
    assert UserName == ResponseBody["user"]["username"]
    assert "createdAt" in ResponseBody["user"]
    assert "modifiedAt" in ResponseBody["user"]

@pytest.mark.api
@pytest.mark.xfail(reason = "Its allowing Duplicate User ")
def test_CreateDuplicateUser(api_client):
    UserBody = make_user_body()
    FirstName = UserBody["firstName"]
    LastName = UserBody["lastName"]
    UserName = UserBody["username"]

    ApiClient = ClientUser(api_client)
    Response = ApiClient.CreateUser(UserBody)
    expect(Response).to_be_ok()
    assert Response.status == 201
    assert Response.status_text == "Created"
    ResponseBody = Response.json()
    assert "id" in ResponseBody["user"]
    assert "uuid" in ResponseBody["user"]
    assert FirstName == ResponseBody["user"]["firstName"]
    assert LastName == ResponseBody["user"]["lastName"]
    assert UserName == ResponseBody["user"]["username"]
    assert "createdAt" in ResponseBody["user"]
    assert "modifiedAt" in ResponseBody["user"]

    DuplicateResponse = ApiClient.CreateUser(UserBody)
    assert DuplicateResponse.status == 409
    assert DuplicateResponse.status_text == "Conflict"

@pytest.mark.api
def test_CreateUserWithMissingData(api_client):
    ApiClient = ClientUser(api_client)
    Response = ApiClient.CreateUser(UserMissingField)
    assert Response.status == 500
    assert Response.status_text == "Internal Server Error"
  
@pytest.mark.api
def test_CreateUserWithInvalidBody(api_client):
    ApiClient = ClientUser(api_client)
    Response = ApiClient.CreateUser(UserBrokenBody)
    assert Response.status == 422
    assert Response.status_text == "Unprocessable Entity"