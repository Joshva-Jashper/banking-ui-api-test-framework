from faker import Faker

faker = Faker()

def make_user_body():
    return {
        "firstName": faker.first_name(),
        "lastName": faker.last_name(),
        "username": faker.user_name() + str(faker.random_int(min=1000, max=99999)),
        "password": faker.password(length=12),
    }

UserMissingField = {
    "firstName": "jhon",
    "lastName": "dacy",
    "username": "joshva"
}

UserBrokenBody = """{
    "firstName": "broken",
    "lastName": "broken",
    "username": "broken"
"""