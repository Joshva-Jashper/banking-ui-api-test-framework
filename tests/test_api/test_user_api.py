import pytest
from playwright.sync_api import expect
from pages.pages_api.client_login import UserLogin
from pages.pages_api.client_user import ClientUser
from test_data.user_api import make_user_body
from faker import Faker

@pytest.mark.api
@pytest.mark.smoke
def test_GetUserWithUserId(api_client):
    UserBody = make_user_body()
    UserRegisterClient = ClientUser(api_client)
    UserLoginClient = UserLogin(api_client)
    RegisterResponse = UserRegisterClient.CreateUser(UserBody)
    expect(RegisterResponse).to_be_ok()
    assert RegisterResponse.status == 201
    assert RegisterResponse.status_text == "Created"
    RegisterResponseBody = RegisterResponse.json()
    UserId = RegisterResponseBody["user"]["id"]
    LoginResponse = UserLoginClient.CreateLogin(UserBody["username"], UserBody["password"])
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
    UserBody = make_user_body()
    UserRegisterClient = ClientUser(api_client)
    UserLoginClient = UserLogin(api_client)
    RegisterResponse = UserRegisterClient.CreateUser(UserBody)
    expect(RegisterResponse).to_be_ok()
    assert RegisterResponse.status == 201
    assert RegisterResponse.status_text == "Created"
    RegisterResponseBody = RegisterResponse.json()
    UserId = RegisterResponseBody["user"]["id"]
    LoginResponse = UserLoginClient.CreateLogin(UserBody["username"], UserBody["password"])
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
    assert Response.status == 401
    assert Response.status_text == "Unauthorized"


@pytest.mark.api
def test_SearchQueryWithValidKeyword(api_client):
    UserBody = make_user_body()
    UserRegister1 = ClientUser(api_client)
    UserLogin1 = UserLogin(api_client)
    UserRegister2 = ClientUser(api_client)
    faker = Faker()
    NewUser1Response = UserRegister1.CreateUser(UserBody)
    UserLogin1.CreateLogin(UserBody["username"], UserBody["password"])
    User2FirstName = faker.first_name()
    user2username = faker.user_name()
    user2Password = faker.password()
    user2LastName = faker.last_name()
    UserBody["firstName"] = User2FirstName
    UserBody["username"] = user2username
    UserBody["password"] = user2Password
    UserBody["lastName"] = user2LastName
    
    NewUser2Response = UserRegister2.CreateUser(UserBody)
    NewUser1SearchResponse = UserRegister1.GetUserBySearch(User2FirstName)
    expect(NewUser1SearchResponse).to_be_ok()
    assert NewUser1SearchResponse.status == 200
    assert NewUser1SearchResponse.status_text == "OK"
    NewUser1SearchResponseBody = NewUser1SearchResponse.json()
    Results = NewUser1SearchResponseBody["results"]
    assert any(Result["username"] == NewUser2Response.json()["user"]["username"] for Result in Results)

@pytest.mark.api
def test_SearchQueryWithInvalidKeyword(api_client):
    UserBody = make_user_body()
    UserRegister1 = ClientUser(api_client)
    UserLogin1 = UserLogin(api_client)
    UserRegister2 = ClientUser(api_client)
    faker = Faker()
    NewUser1Response = UserRegister1.CreateUser(UserBody)
    UserLogin1.CreateLogin(UserBody["username"], UserBody["password"])
    userName = faker.user_name()
    User1SearchResponse = UserRegister1.GetUserBySearch(userName)
    assert User1SearchResponse.status == 200
    assert User1SearchResponse.status_text == "OK"
    Results = User1SearchResponse.json()["results"]
    assert (Result["username"] != userName for Result in Results)

@pytest.mark.api
def test_SearchQueryWithSameUserKeyword(api_client):
    UserBody = make_user_body()
    UserRegister = ClientUser(api_client)
    UserVerify = UserLogin(api_client)
    UserRegister.CreateUser(UserBody)
    UserVerify.CreateLogin(UserBody["username"], UserBody["password"])
    UserSearchQueryResponse = UserRegister.GetUserBySearch(UserBody["username"])
    expect(UserSearchQueryResponse).to_be_ok()
    assert UserSearchQueryResponse.status == 200
    assert UserSearchQueryResponse.status_text == "OK"
    UserSearchQueryResponseBody = UserSearchQueryResponse.json()
    Results = UserSearchQueryResponseBody["results"]
    assert all(Result["username"] != UserBody["username"] for Result in Results)

@pytest.mark.api
def test_SearchQueryWithNoKeyWord(api_client):
    UserBody = make_user_body()
    UserRegister = ClientUser(api_client)
    UserVerify = UserLogin(api_client)
    UserRegister.CreateUser(UserBody)
    UserVerify.CreateLogin(UserBody["username"], UserBody["password"])
    UserSearchQueryResponse = UserRegister.GetUserbySearchWithNoKeyWord()
    assert UserSearchQueryResponse.status == 422
    assert UserSearchQueryResponse.status_text == "Unprocessable Entity"


@pytest.mark.api
def test_UpdateUserWithBody(api_client):
    UserBody = make_user_body()
    faker = Faker()
    UserRegister = ClientUser(api_client)
    UserVerify = UserLogin(api_client)
    UserRegisterResponse = UserRegister.CreateUser(UserBody)
    UserId = UserRegisterResponse.json()["user"]["id"]
    UserVerify.CreateLogin(UserBody["username"], UserBody["password"])
    NewFirstName = faker.first_name()
    NewLastName = faker.last_name()
    UserBody["firstName"] = NewFirstName
    UserBody["lastName"] = NewLastName
    UpdatedUserResponse = UserRegister.UpdateUser(UserBody,UserId)
    expect(UpdatedUserResponse).to_be_ok()
    assert UpdatedUserResponse.status == 204
    assert UpdatedUserResponse.status_text == "No Content"
    GetUpdatedUser = UserRegister.GetUser(UserId)
    expect(GetUpdatedUser).to_be_ok()
    assert GetUpdatedUser.status == 200
    assert GetUpdatedUser.status_text == "OK"
    GetUpdatedUserBody = GetUpdatedUser.json()["user"]
    UserRegisterResponseBody = UserRegisterResponse.json()["user"]
    assert UserRegisterResponseBody["id"] == GetUpdatedUserBody["id"]
    assert NewFirstName == GetUpdatedUserBody["firstName"]
    assert NewLastName == GetUpdatedUserBody["lastName"]

@pytest.mark.api
def test_PublicUserProfile(api_client):
    UserRegister = ClientUser(api_client)
    UserBody = make_user_body()
    UserRegisterResponse = UserRegister.CreateUser(UserBody)
    ProfileSearchResponse = UserRegister.GetPublicUserProfile(UserBody["username"])
    expect(ProfileSearchResponse).to_be_ok()
    assert ProfileSearchResponse.status == 200
    assert ProfileSearchResponse.status_text == "OK"
    ProfileSearchResponseBody = ProfileSearchResponse.json()
    assert ProfileSearchResponseBody["user"]["firstName"] == UserRegisterResponse.json()["user"]["firstName"]
    assert ProfileSearchResponseBody["user"]["lastName"] == UserRegisterResponse.json()["user"]["lastName"]    
    

@pytest.mark.api
def test_PublicUserProfileWithInvalidUserName(api_client):
    UserRegister = ClientUser(api_client)
    faker = Faker()
    ProfileSearchResponse = UserRegister.GetPublicUserProfile(faker.user_name())
    assert ProfileSearchResponse.status == 200
    assert ProfileSearchResponse.status_text == "OK"
    assert len(ProfileSearchResponse.json()["user"]) == 0


