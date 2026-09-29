from faker import Faker

faker = Faker()

FirstName = faker.first_name()
LastName = faker.last_name()
UserName = faker.user_name()
Password = faker.password(length=12)

UserBody = {
    "firstName": FirstName,
    "lastName": LastName,
    "username": UserName,
    "password": Password,
}

UserMissingField = {
    "firstName": "jhon",
    "lastName": "dacy",
    "username": "joshva" 
}

UserBrokenBody = f"""{{
    "firstName": "{FirstName}",
    "lastName": "{LastName}",
    "username": "{UserName}",
    "password": "{Password}"
"""