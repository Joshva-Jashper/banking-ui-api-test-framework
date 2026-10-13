from playwright.sync_api import expect
from pages.pages_api.client_user import ClientUser
from pages.pages_api.client_login import UserLogin
from pages.pages_api.client_transaction import ClientTransaction
from pages.pages_api.client_like import ClientLike
from test_data.user_api import make_user_body
from test_data.bank_pay_req import getUserTransactionPaymentBody
from faker import Faker
import pytest

@pytest.mark.api
def test_AddLikeToTransactionWithTransactionId(api_client):
    UserRegister1 = ClientUser(api_client)
    UserRegister2 = ClientUser(api_client)
    UserVerify1 = UserLogin(api_client)
    UserVerify1 = UserLogin(api_client)
    UserTransaction1 = ClientTransaction(api_client)
    UserTransaction1 = ClientTransaction(api_client)
    UserLike = ClientLike(api_client)
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
    TransactionId = PaymentResponseBody["transaction"]["id"]
    GetPaymentResponseBefore = UserTransaction1.GetOneTransaction(TransactionId)
    expect(GetPaymentResponseBefore).to_be_ok()
    assert GetPaymentResponseBefore.status == 200
    assert GetPaymentResponseBefore.status_text == "OK"
    AddTransactionLikeBefore = GetPaymentResponseBefore.json()["transaction"]["likes"]
    assert len(AddTransactionLikeBefore) == 0
    UserLikeTransaction = UserLike.AddLikeWithTransactionId(TransactionId)
    assert UserLikeTransaction.status == 200
    assert UserLikeTransaction.status_text == "OK"
    GetPaymentResponseAfter = UserTransaction1.GetOneTransaction(TransactionId)
    AddTransactionLikeAfter = GetPaymentResponseAfter.json()["transaction"]["likes"]
    assert AddTransactionLikeAfter[0]["userId"] == UserRegisterResponse1.json()["user"]["id"]
    assert AddTransactionLikeAfter[0]["transactionId"] == TransactionId

@pytest.mark.api
def test_AddCommentToTransactionWithTransactionId(api_client):
    UserRegister1 = ClientUser(api_client)
    UserRegister2 = ClientUser(api_client)
    UserVerify1 = UserLogin(api_client)
    faker = Faker()
    UserVerify1 = UserLogin(api_client)
    UserTransaction1 = ClientTransaction(api_client)
    UserTransaction1 = ClientTransaction(api_client)
    UserComment = ClientLike(api_client)
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
    TransactionId = PaymentResponseBody["transaction"]["id"]
    GetPaymentResponseBefore = UserTransaction1.GetOneTransaction(TransactionId)
    expect(GetPaymentResponseBefore).to_be_ok()
    assert GetPaymentResponseBefore.status == 200
    assert GetPaymentResponseBefore.status_text == "OK"
    AddTransactionCommentBefore = GetPaymentResponseBefore.json()["transaction"]["likes"]
    assert len(AddTransactionCommentBefore) == 0
    Comment = faker.text()
    UserCommentTransaction = UserComment.AddCommentWithTransactionId(TransactionId,Comment)
    assert UserCommentTransaction.status == 200
    assert UserCommentTransaction.status_text == "OK"
    GetPaymentResponseAfter = UserTransaction1.GetOneTransaction(TransactionId)
    AddTransactionCommentAfter = GetPaymentResponseAfter.json()["transaction"]["comments"]
    assert AddTransactionCommentAfter[0]["userId"] == UserRegisterResponse1.json()["user"]["id"]
    assert AddTransactionCommentAfter[0]["transactionId"] == TransactionId
    assert AddTransactionCommentAfter[0]["content"] == Comment
    

@pytest.mark.api
def test_AddCommentToTransactionWithInvalidBody(api_client):
    UserRegister1 = ClientUser(api_client)
    UserRegister2 = ClientUser(api_client)
    UserVerify1 = UserLogin(api_client)
    faker = Faker()
    UserVerify1 = UserLogin(api_client)
    UserTransaction1 = ClientTransaction(api_client)
    UserTransaction1 = ClientTransaction(api_client)
    UserComment = ClientLike(api_client)
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
    TransactionId = PaymentResponseBody["transaction"]["id"]
    GetPaymentResponseBefore = UserTransaction1.GetOneTransaction(TransactionId)
    expect(GetPaymentResponseBefore).to_be_ok()
    assert GetPaymentResponseBefore.status == 200
    assert GetPaymentResponseBefore.status_text == "OK"
    AddTransactionCommentBefore = GetPaymentResponseBefore.json()["transaction"]["likes"]
    assert len(AddTransactionCommentBefore) == 0
    Comment = faker.text()
    UserCommentTransaction = UserComment.AddCommentWithTransactionIdWithInvalidBody(TransactionId,Comment)
    assert UserCommentTransaction.status == 422
    assert UserCommentTransaction.status_text == "Unprocessable Entity"
    