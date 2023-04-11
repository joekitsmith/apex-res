from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class User(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: bool

    class Config:
        orm_mode = True


class UserAuth(User):
    password: str
