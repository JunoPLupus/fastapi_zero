import factory

from fastapi_zero.entities import User, UserPublic

user_username = 'bob'
user_email = 'bob@gmail.com'
user_password = 'mypassword'


class UserMockFactory(factory.Factory):
    class Meta:
        model = User

    username = user_username
    email = user_email
    password = user_password


class UserPublicMockFactory(factory.Factory):
    class Meta:
        model = UserPublic

    id = 1
    username = user_username
    email = user_email
