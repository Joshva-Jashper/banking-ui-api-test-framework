from playwright.sync_api import expect
from pages.pages_api.client_login import UserLogin
from pages.pages_api.client_user import ClientUser
from pages.pages_api.client_transaction import ClientTransaction
from test_data.user_api import make_user_body
from test_data.bank_pay_req import getUserTransactionPaymentBody,getUsertransactionRequestBody
import pytest

@pytest.mark.smoke
@pytest.mark.api
def test_DoTransactionpayment(api_client):
    UserRegister1 = ClientUser(api_client)
    UserRegister2 = ClientUser(api_client)
    UserVerify1 = UserLogin(api_client)
    UserVerify1 = UserLogin(api_client)
    UserTransaction1 = ClientTransaction(api_client)
    UserTransaction1 = ClientTransaction(api_client)
    UserBody1 = make_user_body()
    UserBody2 = make_user_body()
    UserRegisterResponse1 = UserRegister1.CreateUser(UserBody1)
    UserRegisterResponse2 = UserRegister2.CreateUser(UserBody2)
    UserLogin1 = UserVerify1.CreateLogin(UserBody1["username"],UserBody1["password"])
    ReceiverId = UserRegisterResponse2.json()["user"]["id"]
    PaymentBody = getUserTransactionPaymentBody()
    PaymentBody["receiverId"] = ReceiverId
    PaymentResponse = UserTransaction1.DoTransactionRequest(PaymentBody)
    expect(PaymentResponse).to_be_ok()
    assert PaymentResponse.status == 200
    assert PaymentResponse.status_text == "OK"
    PaymentResponseBody = PaymentResponse.json()
    assert PaymentResponseBody["transaction"]["senderId"] == UserRegisterResponse1.json()["user"]["id"]
    assert PaymentResponseBody["transaction"]["receiverId"] == UserRegisterResponse2.json()["user"]["id"]
    GetPaymentResponse = UserTransaction1.GetTransaction()
    expect(GetPaymentResponse).to_be_ok()
    assert GetPaymentResponse.status == 200
    assert GetPaymentResponse.status_text == "OK"
    assert GetPaymentResponse.json()["results"][0]["senderName"] == UserRegisterResponse1.json()["user"]["firstName"] + " " + UserRegisterResponse1.json()["user"]["lastName"]
    assert GetPaymentResponse.json()["results"][0]["receiverName"] == UserRegisterResponse2.json()["user"]["firstName"] + " " + UserRegisterResponse2.json()["user"]["lastName"]
    assert GetPaymentResponse.json()["results"][0]["id"] == PaymentResponseBody["transaction"]["id"]

    