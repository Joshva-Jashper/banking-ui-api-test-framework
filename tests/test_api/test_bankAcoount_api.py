from playwright.sync_api import expect
from pages.pages_api.client_bankAccount import BankAccount
from pages.pages_api.client_login import UserLogin
from pages.pages_api.client_user import ClientUser
from test_data.user_api import make_user_body
from test_data.bank_account import makeBankAccount,bankAccountInvalidBody
import pytest

@pytest.mark.api
@pytest.mark.smoke
def test_AddBankAccountWithvalidBody(api_client):
    UserRegister = ClientUser(api_client)
    UserVerify = UserLogin(api_client)
    UserBank = BankAccount(api_client)
    BankBody = makeBankAccount()
    UserBody = make_user_body()
    UserRegister.CreateUser(UserBody)
    UserLoginResponse = UserVerify.CreateLogin(UserBody["username"],UserBody["password"])
    UserLoginBody = UserLoginResponse.json()["user"]
    AddbankAccountResponse = UserBank.AddBankAccount(BankBody)
    expect(AddbankAccountResponse).to_be_ok()
    assert AddbankAccountResponse.status == 200
    assert AddbankAccountResponse.status_text == "OK"
    AddbankAccountResponseBody = AddbankAccountResponse.json()["account"]
    assert AddbankAccountResponseBody["userId"] == UserLoginBody["id"]
    assert AddbankAccountResponseBody["bankName"] == BankBody["bankName"]
    assert AddbankAccountResponseBody["routingNumber"] == BankBody["routingNumber"]
    assert AddbankAccountResponseBody["accountNumber"] == BankBody["accountNumber"]

@pytest.mark.api
def test_AddBankAccountWithInvalidBody(api_client):
    UserRegister = ClientUser(api_client)
    UserVerify = UserLogin(api_client)
    UserBank = BankAccount(api_client)
    UserBody = make_user_body()
    UserRegister.CreateUser(UserBody)
    UserLoginResponse = UserVerify.CreateLogin(UserBody["username"],UserBody["password"])
    UserLoginBody = UserLoginResponse.json()["user"]
    AddbankAccountResponse = UserBank.AddBankAccount(bankAccountInvalidBody)
    assert AddbankAccountResponse.status == 422
    assert AddbankAccountResponse.status_text == "Unprocessable Entity"

@pytest.mark.api
def test_GetAllBankAccounts(api_client):
    UserRegister = ClientUser(api_client)
    UserVerify = UserLogin(api_client)
    UserBank = BankAccount(api_client)
    BankBody = makeBankAccount()
    UserBody = make_user_body()
    UserRegister.CreateUser(UserBody)
    UserLoginResponse = UserVerify.CreateLogin(UserBody["username"],UserBody["password"])
    UserLoginBody = UserLoginResponse.json()["user"]
    AddbankAccountResponse = UserBank.AddBankAccount(BankBody)
    expect(AddbankAccountResponse).to_be_ok()
    assert AddbankAccountResponse.status == 200
    assert AddbankAccountResponse.status_text == "OK"
    AddbankAccountResponseBody = AddbankAccountResponse.json()["account"]
    assert AddbankAccountResponseBody["userId"] == UserLoginBody["id"]
    assert AddbankAccountResponseBody["bankName"] == BankBody["bankName"]
    assert AddbankAccountResponseBody["routingNumber"] == BankBody["routingNumber"]
    assert AddbankAccountResponseBody["accountNumber"] == BankBody["accountNumber"]
    GetAllAcounts = UserBank.GetAllBankAccount()
    expect(GetAllAcounts).to_be_ok()
    assert GetAllAcounts.status == 200
    assert GetAllAcounts.status_text == "OK"
    GetAllAcountsBody = GetAllAcounts.json()["results"]
    for account in GetAllAcountsBody:
        assert (account["userId"] == UserLoginBody["id"])

@pytest.mark.api
def test_GetBankAccountWithBankId(api_client):
    UserRegister = ClientUser(api_client)
    UserVerify = UserLogin(api_client)
    UserBank = BankAccount(api_client)
    BankBody = makeBankAccount()
    UserBody = make_user_body()
    UserRegister.CreateUser(UserBody)
    UserLoginResponse = UserVerify.CreateLogin(UserBody["username"],UserBody["password"])
    UserLoginBody = UserLoginResponse.json()["user"]
    AddbankAccountResponse = UserBank.AddBankAccount(BankBody)
    expect(AddbankAccountResponse).to_be_ok()
    assert AddbankAccountResponse.status == 200
    assert AddbankAccountResponse.status_text == "OK"
    AddbankAccountResponseBody = AddbankAccountResponse.json()["account"]
    assert AddbankAccountResponseBody["userId"] == UserLoginBody["id"]
    assert AddbankAccountResponseBody["bankName"] == BankBody["bankName"]
    assert AddbankAccountResponseBody["routingNumber"] == BankBody["routingNumber"]
    assert AddbankAccountResponseBody["accountNumber"] == BankBody["accountNumber"]
    GetAccount = UserBank.GetbankAccountWithId(AddbankAccountResponseBody["id"])
    expect(GetAccount).to_be_ok()
    assert GetAccount.status == 200
    assert GetAccount.status_text == "OK"
    GetAccountBody = GetAccount.json()["account"]
    assert AddbankAccountResponseBody["id"] == GetAccountBody["id"]
    assert AddbankAccountResponseBody["uuid"] == GetAccountBody["uuid"]
    assert AddbankAccountResponseBody["userId"] == GetAccountBody["userId"]
    assert AddbankAccountResponseBody["bankName"] == GetAccountBody["bankName"]
    assert AddbankAccountResponseBody["accountNumber"] == GetAccountBody["accountNumber"]
    assert AddbankAccountResponseBody["routingNumber"] == GetAccountBody["routingNumber"]
    assert AddbankAccountResponseBody["createdAt"] == GetAccountBody["createdAt"]
    assert AddbankAccountResponseBody["modifiedAt"] == GetAccountBody["modifiedAt"]

@pytest.mark.api
def test_DeleteBankAccount(api_client):
    UserRegister = ClientUser(api_client)
    UserVerify = UserLogin(api_client)
    UserBank = BankAccount(api_client)
    BankBody = makeBankAccount()
    UserBody = make_user_body()
    UserRegister.CreateUser(UserBody)
    UserLoginResponse = UserVerify.CreateLogin(UserBody["username"],UserBody["password"])
    UserLoginBody = UserLoginResponse.json()["user"]
    AddbankAccountResponse = UserBank.AddBankAccount(BankBody)
    expect(AddbankAccountResponse).to_be_ok()
    assert AddbankAccountResponse.status == 200
    assert AddbankAccountResponse.status_text == "OK"
    AddbankAccountResponseBody = AddbankAccountResponse.json()["account"]
    assert AddbankAccountResponseBody["userId"] == UserLoginBody["id"]
    assert AddbankAccountResponseBody["bankName"] == BankBody["bankName"]
    assert AddbankAccountResponseBody["routingNumber"] == BankBody["routingNumber"]
    assert AddbankAccountResponseBody["accountNumber"] == BankBody["accountNumber"]
    GetAccountBeforeDelete = UserBank.GetbankAccountWithId(AddbankAccountResponseBody["id"])
    assert GetAccountBeforeDelete.json()["account"]["isDeleted"] == False
    DeleteAccount = UserBank.DeleteBankAccountWithId(AddbankAccountResponseBody["id"])
    expect(DeleteAccount).to_be_ok()
    assert DeleteAccount.status == 200
    assert DeleteAccount.status_text == "OK"
    GetAccountAfterDelete = UserBank.GetbankAccountWithId(AddbankAccountResponseBody["id"])
    assert GetAccountAfterDelete.json()["account"]["isDeleted"] == True

    
    
    