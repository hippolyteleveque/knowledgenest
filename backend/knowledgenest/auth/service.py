from uuid import UUID
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import time
from typing import Annotated, Optional
import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError
from sqlalchemy.orm.session import Session
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from knowledgenest.auth.models import User, UserSetting
from knowledgenest.auth.schema import UserBase
from knowledgenest.auth.utils import create_hash
from knowledgenest.database import DbSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

SECRET_KEY = os.getenv("OAUTH_SECRET_KEY")
SECRET_KEY = SECRET_KEY or "dev-secret"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=3)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, expire


def verify_access_token(token: str) -> bool:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token["exp"] >= time.time()
    except (KeyError, ExpiredSignatureError, JWTError):
        return False


def create_user(email: str, password: str, db: Session):
    hashed_password_binary = create_hash(password)
    hashed_password = hashed_password_binary.decode("utf-8")
    new_user = User(email=email, password=hashed_password)
    setting = UserSetting(user=new_user)
    db.add(new_user)
    db.add(setting)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail=f"User with email {email} not found"
        )
    return user


def curr_user(db: DbSession, token: str) -> User:
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload["username"]
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(username, db)
    if user is None:
        raise credentials_exception
    return user


def get_current_user(
    db: DbSession, token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    user = curr_user(db, token)
    return user


CurrentUser = Annotated[UserBase, Depends(get_current_user)]


def update_user_settings(ai_provider: str, user_id: UUID, db: Session) -> UserSetting:
    setting = db.query(UserSetting).filter(UserSetting.user_id == user_id).first()
    if not setting:
        raise ValueError(f"Did not found any settings attached to user {user_id}")
    setting.ai_provider = ai_provider
    db.commit()
    db.refresh(setting)
    return setting
