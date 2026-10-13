from playwright.sync_api import expect
from pages.pages_api.client_login import UserLogin
from pages.pages_api.client_user import ClientUser
from pages.pages_api.client_transaction import ClientTransaction
from test_data.user_api import make_user_body
from test_data.bank_pay_req import getUserTransactionPaymentBody,getUsertransactionRequestBody
import pytest

@pytest.mark.smoke
@pytest.mark.api
def test_DoTransactionPayment(api_client):
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


@pytest.mark.api
def test_DoTransactionRequestAccept(api_client):
    UserRegister1 = ClientUser(api_client)
    UserRegister2 = ClientUser(api_client)
    UserVerify1 = UserLogin(api_client)
    UserVerify2 = UserLogin(api_client)
    UserTransaction1 = ClientTransaction(api_client)
    UserBody1 = make_user_body()
    UserBody2 = make_user_body()
    PaymentBody = getUsertransactionRequestBody()
    UserRegister1Response = UserRegister1.CreateUser(UserBody1)
    UserRegister2Response = UserRegister2.CreateUser(UserBody2)
    UserVerify2.CreateLogin(UserBody2["username"],UserBody2["password"])
    UserVerify1.CreateLogin(UserBody1["username"],UserBody1["password"])
    ReceiverId = UserRegister2Response.json()["user"]["id"]
    PaymentBody["receiverId"] = ReceiverId
    DoPaymentRequest = UserTransaction1.DoTransactionRequest(PaymentBody)
    expect(DoPaymentRequest).to_be_ok()
    assert DoPaymentRequest.status == 200
    assert DoPaymentRequest.status_text == "OK"
    DoPaymentRequestBody = DoPaymentRequest.json()
    assert DoPaymentRequestBody["transaction"]["receiverId"] == UserRegister2Response.json()["user"]["id"]
    assert DoPaymentRequestBody["transaction"]["senderId"] == UserRegister1Response.json()["user"]["id"]
    assert DoPaymentRequestBody["transaction"]["status"] == "pending"
    UserVerify2.CreateLogin(UserBody2["username"],UserBody2["password"])
    TransactionId = DoPaymentRequestBody["transaction"]["id"]
    AcceptPayment = UserTransaction1.UpdateTransaction(TransactionId,{"requestStatus" : "accepted"})
    expect(AcceptPayment).to_be_ok()
    assert AcceptPayment.status == 204
    assert AcceptPayment.status_text == "No Content"
    AfterPaymentRequestAccept = UserTransaction1.GetOneTransaction(TransactionId)
    expect(AfterPaymentRequestAccept).to_be_ok()
    AfterPaymentRequestAccept.status == 200
    AfterPaymentRequestAccept.status_text == "OK"
    AfterPaymentRequestAcceptBody = AfterPaymentRequestAccept.json()["transaction"]
    assert AfterPaymentRequestAcceptBody["status"] == "complete"
    assert AfterPaymentRequestAcceptBody["requestStatus"] == "accepted"
    assert AfterPaymentRequestAcceptBody["senderId"] == UserRegister1Response.json()["user"]["id"]
    assert AfterPaymentRequestAcceptBody["receiverId"] == UserRegister2Response.json()["user"]["id"]
    
    

@pytest.mark.api
def test_DoTransactionRequestReject(api_client):
    UserRegister1 = ClientUser(api_client)
    UserRegister2 = ClientUser(api_client)
    UserVerify1 = UserLogin(api_client)
    UserVerify2 = UserLogin(api_client)
    UserTransaction1 = ClientTransaction(api_client)
    UserBody1 = make_user_body()
    UserBody2 = make_user_body()
    PaymentBody = getUsertransactionRequestBody()
    UserRegister1Response = UserRegister1.CreateUser(UserBody1)
    UserRegister2Response = UserRegister2.CreateUser(UserBody2)
    UserVerify2.CreateLogin(UserBody2["username"],UserBody2["password"])
    UserVerify1.CreateLogin(UserBody1["username"],UserBody1["password"])
    ReceiverId = UserRegister2Response.json()["user"]["id"]
    PaymentBody["receiverId"] = ReceiverId
    DoPaymentRequest = UserTransaction1.DoTransactionRequest(PaymentBody)
    expect(DoPaymentRequest).to_be_ok()
    assert DoPaymentRequest.status == 200
    assert DoPaymentRequest.status_text == "OK"
    DoPaymentRequestBody = DoPaymentRequest.json()
    assert DoPaymentRequestBody["transaction"]["receiverId"] == UserRegister2Response.json()["user"]["id"]
    assert DoPaymentRequestBody["transaction"]["senderId"] == UserRegister1Response.json()["user"]["id"]
    assert DoPaymentRequestBody["transaction"]["status"] == "pending"
    UserVerify2.CreateLogin(UserBody2["username"],UserBody2["password"])
    TransactionId = DoPaymentRequestBody["transaction"]["id"]
    AcceptPayment = UserTransaction1.UpdateTransaction(TransactionId,{"requestStatus" : "rejected"})
    expect(AcceptPayment).to_be_ok()
    assert AcceptPayment.status == 204
    assert AcceptPayment.status_text == "No Content"
    AfterPaymentRequestAccept = UserTransaction1.GetOneTransaction(TransactionId)
    expect(AfterPaymentRequestAccept).to_be_ok()
    AfterPaymentRequestAccept.status == 200
    AfterPaymentRequestAccept.status_text == "OK"
    AfterPaymentRequestAcceptBody = AfterPaymentRequestAccept.json()["transaction"]
    assert AfterPaymentRequestAcceptBody["status"] == "complete"
    assert AfterPaymentRequestAcceptBody["requestStatus"] == "rejected"
    assert AfterPaymentRequestAcceptBody["senderId"] == UserRegister1Response.json()["user"]["id"]
    assert AfterPaymentRequestAcceptBody["receiverId"] == UserRegister2Response.json()["user"]["id"]
    
        

@pytest.mark.api
def test_GetAllPublicTransaction(api_client):
    UserRegister = ClientUser(api_client)
    UserVerify = UserLogin(api_client)
    UserTransaction = ClientTransaction(api_client)
    UserBody = make_user_body()
    UserRegisterResponse = UserRegister.CreateUser(UserBody)
    UserVerify.CreateLogin(UserBody["username"],UserBody["password"])
    AllPublicTransaction = UserTransaction.GetAllPublicTransaction()
    assert AllPublicTransaction.status == 200
    assert AllPublicTransaction.status_text == "OK"

@pytest.mark.api
def test_GetAllTransactionContact(api_client):
    UserRegister = ClientUser(api_client)
    UserVerify = UserLogin(api_client)
    UserTransaction = ClientTransaction(api_client)
    UserBody = make_user_body()
    UserRegisterResponse = UserRegister.CreateUser(UserBody)
    UserVerify.CreateLogin(UserBody["username"],UserBody["password"])
    AllPublicTransaction = UserTransaction.GetAllContactTransaction()
    assert AllPublicTransaction.status == 200
    assert AllPublicTransaction.status_text == "OK"  

@pytest.mark.api
def test_GetTransactionByTransactionId(api_client):
    UserRegister1 = ClientUser(api_client)
    UserRegister2 = ClientUser(api_client)
    UserVerify1 = UserLogin(api_client)
    UserVerify2 = UserLogin(api_client)
    UserTransaction1 = ClientTransaction(api_client)
    UserBody1 = make_user_body()
    UserBody2 = make_user_body()
    PaymentBody = getUsertransactionRequestBody()
    UserRegister1Response = UserRegister1.CreateUser(UserBody1)
    UserRegister2Response = UserRegister2.CreateUser(UserBody2)
    UserVerify2.CreateLogin(UserBody2["username"],UserBody2["password"])
    UserVerify1.CreateLogin(UserBody1["username"],UserBody1["password"])
    ReceiverId = UserRegister2Response.json()["user"]["id"]
    PaymentBody["receiverId"] = ReceiverId
    DoPaymentRequest = UserTransaction1.DoTransactionRequest(PaymentBody)
    expect(DoPaymentRequest).to_be_ok()
    assert DoPaymentRequest.status == 200
    assert DoPaymentRequest.status_text == "OK"
    DoPaymentRequestBody = DoPaymentRequest.json()
    assert DoPaymentRequestBody["transaction"]["receiverId"] == UserRegister2Response.json()["user"]["id"]
    assert DoPaymentRequestBody["transaction"]["senderId"] == UserRegister1Response.json()["user"]["id"]
    TransactionId = DoPaymentRequestBody["transaction"]["id"]
    AfterPaymentRequestAccept = UserTransaction1.GetOneTransaction(TransactionId)
    expect(AfterPaymentRequestAccept).to_be_ok()
    AfterPaymentRequestAccept.status == 200
    AfterPaymentRequestAccept.status_text == "OK"
    AfterPaymentRequestAcceptBody = AfterPaymentRequestAccept.json()["transaction"]
    assert AfterPaymentRequestAcceptBody["senderId"] == UserRegister1Response.json()["user"]["id"]
    assert AfterPaymentRequestAcceptBody["receiverId"] == UserRegister2Response.json()["user"]["id"]

    
@pytest.mark.api
def test_TransactionByInvalidTransactionId(api_client):
    UserRegister1 = ClientUser(api_client)
    UserRegister2 = ClientUser(api_client)
    UserVerify1 = UserLogin(api_client)
    UserVerify2 = UserLogin(api_client)
    UserTransaction1 = ClientTransaction(api_client)
    UserBody1 = make_user_body()
    UserBody2 = make_user_body()
    PaymentBody = getUsertransactionRequestBody()
    UserRegister1Response = UserRegister1.CreateUser(UserBody1)
    UserRegister2Response = UserRegister2.CreateUser(UserBody2)
    UserVerify2.CreateLogin(UserBody2["username"],UserBody2["password"])
    UserVerify1.CreateLogin(UserBody1["username"],UserBody1["password"])
    ReceiverId = UserRegister2Response.json()["user"]["id"]
    PaymentBody["receiverId"] = ReceiverId
    DoPaymentRequest = UserTransaction1.DoTransactionRequest(PaymentBody)
    expect(DoPaymentRequest).to_be_ok()
    assert DoPaymentRequest.status == 200
    assert DoPaymentRequest.status_text == "OK"
    DoPaymentRequestBody = DoPaymentRequest.json()
    assert DoPaymentRequestBody["transaction"]["receiverId"] == UserRegister2Response.json()["user"]["id"]
    assert DoPaymentRequestBody["transaction"]["senderId"] == UserRegister1Response.json()["user"]["id"]
    AfterPaymentRequestAccept = UserTransaction1.GetOneTransaction("12343")
    AfterPaymentRequestAccept.status == 422
    AfterPaymentRequestAccept.status_text == "Unprocessable Entity"

@pytest.mark.api
def test_TransactionFilterStatus(api_client):
    UserRegister1 = ClientUser(api_client)
    UserRegister2 = ClientUser(api_client)
    UserVerify1 = UserLogin(api_client)
    UserVerify2 = UserLogin(api_client)
    UserTransaction1 = ClientTransaction(api_client)
    UserBody1 = make_user_body()
    UserBody2 = make_user_body()
    PaymentBody = getUsertransactionRequestBody()
    UserRegister1Response = UserRegister1.CreateUser(UserBody1)
    UserRegister2Response = UserRegister2.CreateUser(UserBody2)
    UserVerify2.CreateLogin(UserBody2["username"],UserBody2["password"])
    UserVerify1.CreateLogin(UserBody1["username"],UserBody1["password"])
    ReceiverId = UserRegister2Response.json()["user"]["id"]
    PaymentBody["receiverId"] = ReceiverId
    DoPaymentRequest = UserTransaction1.DoTransactionRequest(PaymentBody)
    GetTransaction = UserTransaction1.GetTransactionFilterSatus("pending")
    expect(GetTransaction).to_be_ok()
    assert GetTransaction.status == 200
    assert GetTransaction.status_text == "OK"
    Results =  GetTransaction.json()["results"]
    for result in Results:
        assert result["status"] == "pending"

@pytest.mark.api
def test_TransactionFilterRequestStatus(api_client):
    UserRegister1 = ClientUser(api_client)
    UserRegister2 = ClientUser(api_client)
    UserVerify1 = UserLogin(api_client)
    UserVerify2 = UserLogin(api_client)
    UserTransaction1 = ClientTransaction(api_client)
    UserBody1 = make_user_body()
    UserBody2 = make_user_body()
    PaymentBody = getUsertransactionRequestBody()
    UserRegister1Response = UserRegister1.CreateUser(UserBody1)
    UserRegister2Response = UserRegister2.CreateUser(UserBody2)
    UserVerify2.CreateLogin(UserBody2["username"],UserBody2["password"])
    UserVerify1.CreateLogin(UserBody1["username"],UserBody1["password"])
    ReceiverId = UserRegister2Response.json()["user"]["id"]
    PaymentBody["receiverId"] = ReceiverId
    DoPaymentRequest = UserTransaction1.DoTransactionRequest(PaymentBody)
    expect(DoPaymentRequest).to_be_ok()
    assert DoPaymentRequest.status == 200
    assert DoPaymentRequest.status_text == "OK"
    DoPaymentRequestBody = DoPaymentRequest.json()
    assert DoPaymentRequestBody["transaction"]["receiverId"] == UserRegister2Response.json()["user"]["id"]
    assert DoPaymentRequestBody["transaction"]["senderId"] == UserRegister1Response.json()["user"]["id"]
    assert DoPaymentRequestBody["transaction"]["status"] == "pending"
    UserVerify2.CreateLogin(UserBody2["username"],UserBody2["password"])
    TransactionId = DoPaymentRequestBody["transaction"]["id"]
    AcceptPayment = UserTransaction1.UpdateTransaction(TransactionId,{"requestStatus" : "rejected"})
    GetTransaction = UserTransaction1.GetTransactionFilterRequestStatus("rejected")
    expect(GetTransaction).to_be_ok()
    assert GetTransaction.status == 200
    assert GetTransaction.status_text == "OK"
    Results =  GetTransaction.json()["results"]
    for result in Results:
        assert result["requestStatus"] == "rejected"
        

        