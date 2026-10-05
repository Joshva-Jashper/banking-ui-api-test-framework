import pytest
from playwright.sync_api import expect
from pages.pages_api.client_login import UserLogin
from pages.pages_api.client_user import ClientUser
from test_data.user_api import UserBody,UserName,FirstName,LastName,Password
from faker import Faker

@pytest.mark.api
@pytest.mark.smoke
def test_GetUserWithUserId(api_client):
    UserRegisterClient = ClientUser(api_client)
    UserLoginClient = UserLogin(api_client)
    RegisterResponse = UserRegisterClient.CreateUser(UserBody)
    expect(RegisterResponse).to_be_ok()
    assert RegisterResponse.status == 201
    assert RegisterResponse.status_text == "Created"
    RegisterResponseBody = RegisterResponse.json()
    UserId = RegisterResponseBody["user"]["id"]
    LoginResponse = UserLoginClient.CreateLogin(UserName, Password)
    expect(LoginResponse).to_be_ok()
    assert LoginResponse.status == 200
    assert LoginResponse.status_text == "OK"
    LoginResponseBody = LoginResponse.json()

    UserId = LoginResponseBody["user"]["id"]
    GetUserResponse = UserRegisterClient.GetUser(UserId)
    expect(GetUserResponse).to_be_ok()
    assert GetUserResponse.status == 200
    assert GetUserResponse.status_text == "OK"
    GetUserBody = GetUserResponse.json()["user"]
    assert GetUserBody["id"] == RegisterResponseBody["user"]["id"]
    assert GetUserBody["uuid"] == RegisterResponseBody["user"]["uuid"]
    assert GetUserBody["firstName"] == RegisterResponseBody["user"]["firstName"]
    assert GetUserBody["lastName"] == RegisterResponseBody["user"]["lastName"]
    assert GetUserBody["username"] == RegisterResponseBody["user"]["username"]
    assert GetUserBody["password"] == RegisterResponseBody["user"]["password"]
    assert GetUserBody["balance"] == RegisterResponseBody["user"]["balance"]
    assert GetUserBody["createdAt"] == RegisterResponseBody["user"]["createdAt"]
    assert GetUserBody["modifiedAt"] == RegisterResponseBody["user"]["modifiedAt"]
    

@pytest.mark.api
def test_getUserWithInvalidUserId(api_client):
    faker = Faker()
    UserClient = ClientUser(api_client)
    Response = UserClient.GetUser(faker.random_int(min=200909,max=741442423424))
    assert Response.status == 401
    assert Response.status_text == "Unauthorized"


@pytest.mark.api
@pytest.mark.smoke
def test_CheckAuthWithValidCookie(api_client):
    UserRegisterClient = ClientUser(api_client)
    UserLoginClient = UserLogin(api_client)
    RegisterResponse = UserRegisterClient.CreateUser(UserBody)
    expect(RegisterResponse).to_be_ok()
    assert RegisterResponse.status == 201
    assert RegisterResponse.status_text == "Created"
    RegisterResponseBody = RegisterResponse.json()
    UserId = RegisterResponseBody["user"]["id"]
    LoginResponse = UserLoginClient.CreateLogin(UserName, Password)
    expect(LoginResponse).to_be_ok()
    assert LoginResponse.status == 200
    assert LoginResponse.status_text == "OK"

    CheckAuthResponse = UserRegisterClient.GetCheckAuth()
    expect(CheckAuthResponse).to_be_ok()
    AuthBody = CheckAuthResponse.json()["user"]
    assert AuthBody["id"] == RegisterResponseBody["user"]["id"]
    assert AuthBody["uuid"] == RegisterResponseBody["user"]["uuid"]
    assert AuthBody["firstName"] == RegisterResponseBody["user"]["firstName"]
    assert AuthBody["lastName"] == RegisterResponseBody["user"]["lastName"]
    assert AuthBody["username"] == RegisterResponseBody["user"]["username"]
    assert AuthBody["password"] == RegisterResponseBody["user"]["password"]
    assert AuthBody["balance"] == RegisterResponseBody["user"]["balance"]
    assert AuthBody["createdAt"] == RegisterResponseBody["user"]["createdAt"]
    assert AuthBody["modifiedAt"] == RegisterResponseBody["user"]["modifiedAt"]
        
    
@pytest.mark.api
def test_CheckAuthWithInvalidCookie(api_client):
    UserApiClient = ClientUser(api_client)
    Response = UserApiClient.GetCheckAuth()
    print(Response)
    assert Response.status == 401
    assert Response.status_text == "Unauthorized"