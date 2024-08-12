from pydantic import UUID4, BaseModel


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


class UserBase(BaseModel):
    id: UUID4
    email: str
    password: str
