from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from api.auth.utils import verify_hash
from api.database import DbSession
from api.auth.service import (
    create_access_token,
    create_user,
    get_user_by_email,
    verify_access_token,
)
from api.auth.schema import SignupUserIn, SignupUserOut, TokenIn
from starlette.responses import Response

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login")
def login(db: DbSession, request: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(request.username, db)
    if not verify_hash(request.password, user.password):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bad credentials"
        )

    access_token = create_access_token(data={"username": request.username})

    return {
        "access_token": access_token,
        "token-type": "bearer",
        "user_id": 1,
        "email": request.username,
    }


@router.post("/signup", response_model=SignupUserOut)
def signup(request: SignupUserIn, db: DbSession):
    new_user = create_user(request.email, request.password, db)
    return new_user


@router.post("/verify")
def verify(request: TokenIn):
    if verify_access_token(request.token):
        return Response(status_code=HTTP_200_OK)
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Incorrect Token")
