from pydantic import BaseModel


class SignupUserIn(BaseModel):
    email: str
    password: str


class SignupUserOut(BaseModel):
    email: str


class TokenIn(BaseModel):
    token: str


class UserIn(BaseModel):
    email: str
    password: str
