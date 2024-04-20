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

from api.auth.models import User
from api.auth.schema import UserBase
from api.auth.utils import create_hash
from api.database import DbSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = os.getenv("OAUTH_SECRET_KEY")
SECRET_KEY = SECRET_KEY or "dev-secret"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str) -> bool:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token["exp"] >= time.time()
    except (KeyError, ExpiredSignatureError):
        return False


def create_user(email: str, password: str, db: Session):
    hashed_password_binary = create_hash(password)
    hashed_password = hashed_password_binary.decode("utf-8")
    new_user = User(email=email, password=hashed_password)
    db.add(new_user)
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


def get_current_user(
    db: DbSession, token: Annotated[str, Depends(oauth2_scheme)]
) -> UserBase:
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


CurrentUser = Annotated[UserBase, Depends(get_current_user)]
