from typing import Literal
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


class UserSettings(BaseModel):
    ai_provider: Literal["mistral", "anthropic", "openai"]


class UserBase(BaseModel):
    id: UUID4
    email: str
    setting: UserSettings
    password: str


class UserOut(BaseModel):
    email: str
    setting: UserSettings
