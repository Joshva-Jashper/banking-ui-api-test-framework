from playwright.sync_api import expect
from pages.pages_api.client_login import UserLogin
from pages.pages_api.client_user import ClientUser
from test_data.user_api import UserBody,UserName,FirstName,LastName,Password
import pytest

@pytest.mark.api
def test_LoginWithValidCredentials(api_client):
    ApiClientLogin = UserLogin(api_client)
    ApiClientUser = ClientUser(api_client)
    Response = ApiClientUser.CreateUser(UserBody)
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

    LoginResponse = ApiClientLogin.CreateLogin(UserName,Password,remember = True)
    expect(LoginResponse).to_be_ok()
    assert LoginResponse.status == 200
    assert LoginResponse.status_text == "OK"
    LoginResponseBody = LoginResponse.json()
    assert ResponseBody["user"]["id"] == LoginResponseBody["user"]["id"]
    assert ResponseBody["user"]["firstName"] == LoginResponseBody["user"]["firstName"]
    assert ResponseBody["user"]["lastName"] == LoginResponseBody["user"]["lastName"]
    assert ResponseBody["user"]["username"] == LoginResponseBody["user"]["username"]
    assert ResponseBody["user"]["password"] == LoginResponseBody["user"]["password"]


@pytest.mark.api
def test_LoginWithInvalidCredentials(api_client):
    LoginApiClient = UserLogin(api_client)
    Response = LoginApiClient.CreateLogin("josh","12344233")
    expect(Response).not_to_be_ok()
    assert Response.status == 401
    assert Response.status_text == "Unauthorized"