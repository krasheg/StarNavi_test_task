from ninja import Schema


class RegisterUserSchema(Schema):
    username: str
    password: str


class LoginUserSchema(Schema):
    username: str
    password: str
