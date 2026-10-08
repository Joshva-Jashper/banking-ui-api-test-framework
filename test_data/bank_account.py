from faker import Faker

def makeBankAccount():
    faker = Faker()
    return {
        "bankName": faker.company(),
        "accountNumber": faker.bban(),
        "routingNumber": faker.aba(),
    }

bankAccountInvalidBody = {
    "bankName": "Axis Bank",
    "accountNumber": "123456789"
}
