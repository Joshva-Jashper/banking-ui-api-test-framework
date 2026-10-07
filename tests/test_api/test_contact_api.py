from pages.pages_api.client_contact import UserContact
from pages.pages_api.client_user import ClientUser
from pages.pages_api.client_login import UserLogin
from test_data.user_api import make_user_body
from playwright.sync_api import expect
from faker import Faker
import pytest

@pytest.mark.api
def test_AddContactValidity(api_client):
    UserRegister1 = ClientUser(api_client)
    UserRegister2 = ClientUser(api_client)
    UserVerify1 = UserLogin(api_client)
    UserVerify2 = UserLogin(api_client)
    ClientContact = UserContact(api_client)
    UserBody1 = make_user_body()
    UserBody2 = make_user_body()

    UserRegister1.CreateUser(UserBody1)
    UserRegister2.CreateUser(UserBody2)

    UserLogin1 = UserVerify1.CreateLogin(UserBody1["username"],UserBody1["password"])
    UserLogin2 = UserVerify2.CreateLogin(UserBody2["username"],UserBody2["password"])
    AddContactResponse = ClientContact.AddContacts(UserLogin2.json()["user"]["id"])
    expect(AddContactResponse).to_be_ok()
    assert AddContactResponse.status == 200
    assert AddContactResponse.status_text == "OK"
    assert AddContactResponse.json()["contact"]["contactUserId"] == UserLogin2.json()["user"]["id"]


@pytest.mark.api
def test_GetvalidContact(api_client):
    UserRegister1 = ClientUser(api_client)
    UserRegister2 = ClientUser(api_client)
    UserVerify1 = UserLogin(api_client)
    UserVerify2 = UserLogin(api_client)
    faker = Faker()
    ClientContact = UserContact(api_client)
    UserBody1 = make_user_body()
    UserBody2 = make_user_body()
    UserRegister1.CreateUser(UserBody1)
    UserRegister2.CreateUser(UserBody2)
    UserVerify1.CreateLogin(UserBody1["username"],UserBody1["password"])
    UserLoginResponse2 = UserVerify2.CreateLogin(UserBody2["username"],UserBody2["password"])
    ContactUserId = UserLoginResponse2.json()["user"]["id"]
    ContactUserName = UserLoginResponse2.json()["user"]["username"]

    AddContactResponse = ClientContact.AddContacts(f"{ContactUserId}")
    expect(AddContactResponse).to_be_ok()
    assert AddContactResponse.status == 200
    assert AddContactResponse.status_text == "OK"
    assert AddContactResponse.json()["contact"]["contactUserId"] ==  f"{ContactUserId}"

    GetContactResponse = ClientContact.GetContacts(ContactUserName)
    assert GetContactResponse.status == 200
    assert GetContactResponse.status_text == "OK"
    assert AddContactResponse.json()["contact"]["id"] == GetContactResponse.json()["contacts"][0]["id"]
    assert AddContactResponse.json()["contact"]["uuid"] == GetContactResponse.json()["contacts"][0]["uuid"]
    assert AddContactResponse.json()["contact"]["userId"] == GetContactResponse.json()["contacts"][0]["userId"]
    assert AddContactResponse.json()["contact"]["contactUserId"] == GetContactResponse.json()["contacts"][0]["contactUserId"]



@pytest.mark.api
def test_GetInvalidContact(api_client):
    UserRegister1 = ClientUser(api_client)
    UserVerify1 = UserLogin(api_client)
    ClientContact = UserContact(api_client)
    faker = Faker()
    UserBody1 = make_user_body() 
    UserRegister1.CreateUser(UserBody1)
    UserVerify1.CreateLogin(UserBody1["username"],UserBody1["password"])
    GetContactResponse = ClientContact.GetContacts("ritik")
    assert GetContactResponse.status == 500
    assert GetContactResponse.status_text == "Internal Server Error"


@pytest.mark.api
def test_DeleteContact(api_client):
    UserRegister1 = ClientUser(api_client)
    UserRegister2 = ClientUser(api_client)
    UserVerify1 = UserLogin(api_client)
    UserVerify2 = UserLogin(api_client)
    ClientContact = UserContact(api_client)
    
    UserBody1 = make_user_body()
    UserBody2 = make_user_body()
    UserRegister1.CreateUser(UserBody1)
    UserRegister2.CreateUser(UserBody2)
    UserVerify1.CreateLogin(UserBody1["username"],UserBody1["password"])
    UserLoginResponse = UserVerify2.CreateLogin(UserBody2["username"],UserBody2["password"])
    AddContactResponse = ClientContact.AddContacts(UserLoginResponse.json()["user"]["id"])
    ContactUserId = AddContactResponse.json()["contact"]["contactUserId"]
    ContactUserName = UserLoginResponse.json()["user"]["username"]
    GetContact = ClientContact.GetContacts(ContactUserName)
    assert GetContact.status == 200
    assert GetContact.status_text == "OK"
    DeleteContact = ClientContact.DeleteContacts(ContactUserId)
    assert DeleteContact.status == 200
    assert DeleteContact.status_text == "OK"
    GetContactAfterDelete = ClientContact.GetContacts(ContactUserName)
    assert GetContactAfterDelete.status == 200
    assert GetContactAfterDelete.status_text == "OK"
    assert len(GetContact.json()["contacts"])-1 == len(GetContactAfterDelete.json()["contacts"])
    

