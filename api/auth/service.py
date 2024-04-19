from fastapi.security import OAuth2PasswordBearer
import time
from typing import Optional
import os
from datetime import datetime, timedelta
from jose import jwt

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
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print(decoded_token)
    try:
        return decoded_token["exp"] >= time.time()
    except KeyError:
        return False
