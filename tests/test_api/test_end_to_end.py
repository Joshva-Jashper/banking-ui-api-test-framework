from pages.pages_ui.login import LoginPage
from pages.pages_api.client_user import ClientUser
from pages.pages_ui.main import MainPage
from pages.pages_ui.register import RegisterPage
from pages.pages_api.client_transaction import ClientTransaction
from pages.pages_ui.new_transaction import NewTransaction
from pages.pages_api.client_login import UserLogin
from faker import Faker
from pages.pages_ui.transaction import Transaction
from test_data.bank_pay_req import getUserTransactionPaymentBody
import pytest
from playwright.sync_api import Page,expect
from test_data.user_api import make_user_body

@pytest.mark.smoke
@pytest.mark.e2e
def test_RegisterLoginE2EFlow(api_client,page : Page):
    UserRegister = ClientUser(api_client)
    UserBody = make_user_body()
    UserRegisterResponse = UserRegister.CreateUser(UserBody)
    assert UserRegisterResponse.status == 201
    assert UserRegisterResponse.status_text == "Created"
    assert UserRegisterResponse.json()["user"]["username"] == UserBody["username"]
    assert UserRegisterResponse.json()["user"]["firstName"] == UserBody["firstName"]
    assert UserRegisterResponse.json()["user"]["lastName"] == UserBody["lastName"]
    page.goto("http://localhost:3000/")
    UserLogin = LoginPage(page)
    expect(UserLogin.get_login_heading()).to_be_visible()
    expect(UserLogin.get_login_heading()).to_contain_text("Sign in")
    UserLogin.SignIn(UserBody["username"],UserBody["password"])
    expect(UserLogin.get_success_login_message()).to_be_visible()
    expect(UserLogin.get_success_login_message()).to_contain_text("Get Started with Real World App")


    
@pytest.mark.e2e
@pytest.mark.xfail(reason = "Transaction is not getting reflected in UI")
def test_TransactionApiUiValidation(api_client,page:Page):
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
    UserVerify1.CreateLogin(UserBody1["username"],UserBody1["password"])
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
    page.goto("http://localhost:3000")
    login_page = LoginPage(page)
    register_page = RegisterPage(page)
    main_page = MainPage(page)
    register_page = RegisterPage(page)
    faker = Faker()
    register_page.click_dont_have_account()
    register_page.click_dont_have_account()
    expect(register_page.get_website_logo()).to_be_visible()
    expect(register_page.get_signUp_heading()).to_be_visible()
    expect(register_page.get_signUp_heading()).to_contain_text("Sign Up")
    user_name = faker.user_name()
    password = faker.password()
    register_page.SignUp(faker.first_name(),faker.last_name(),user_name,password,password)
    login_page = LoginPage(page)
    expect(login_page.get_login_heading()).to_be_visible()
    expect(login_page.get_login_heading()).to_contain_text("Sign in")
    login_page.SignIn(user_name,password)
    expect(login_page.get_success_login_message()).to_be_visible()
    expect(login_page.get_success_login_message()).to_contain_text("Get Started with Real World App")

    expect(main_page.get_getStartedMsg()).to_contain_text("Get Started with Real World App")
    main_page.click_nextStartedMsg()
    main_page.enterBankInfo(faker.bank(),faker.aba(),faker.pystr(min_chars=9,max_chars=12));

    expect(main_page.get_finishedMsg()).to_contain_text("Finished")
    main_page.click_finishedButton()
    transaction_page = Transaction(page)
    transaction_page.clickMyTransaction()
    transaction_page.GetAllTransactionUnderTabs().first.click()
    TransactionSender = transaction_page.GetTransactionSender().inner_text()
    assert TransactionSender == UserRegisterResponse2.json()["user"]["firstName"] + " " + UserRegisterResponse2.json()["user"]["lastName"]
    
    
    
    
        
    

    


