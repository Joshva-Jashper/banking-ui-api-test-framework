from faker import Faker

faker = Faker()

def getUserTransactionPaymentBody():
    return {
        "transactionType" : "payment",
        "receiverId" : "123",
        "amount" : faker.random_int(min=1,max=500),
        "description" : f"{faker.text()}"
    }
    
def getUsertransactionRequestBody():
    return {
        "transactionType" : "request",
        "receiverId" : "123",
        "amount" : faker.random_int(min=1,max=500),
        "description" : f"{faker.text()}"
    }