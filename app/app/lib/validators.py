import pydantic
from lib.err_handler import HttpError


class UserValidator(pydantic.BaseModel):
    username: str
    password: str
    email: str

    @pydantic.validator('password')
    def strong_pass(cls, value):
        if len(value) < 9:
            raise ValueError('password length must be more than 9 characters')
        return value

    @pydantic.validator('username')
    def user_exist(cls, value):
        current_session = Session()
        input_data = dict(fk_request.json)
        user_data = current_session.query(UserModel).filter(UserModel.username == input_data['username']).first()
        if user_data:
            raise HttpErrors(f"a user with the same name ({input_data['username']}) already exists")
        return value

    @pydantic.validator('email')
    def email_exist(cls, value):
        current_session = Session()
        input_data = dict(fk_request.json)
        user_data = current_session.query(UserModel).filter(UserModel.email == input_data['email']).first()
        if user_data:
            raise HttpErrors(f"a user with the same email ({input_data['email']}) already exists")
        return value