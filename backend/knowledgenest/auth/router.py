from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from knowledgenest.auth.utils import verify_hash
from knowledgenest.database import DbSession
from knowledgenest.auth.service import (
    CurrentUser,
    create_access_token,
    create_user,
    get_user_by_email,
    verify_access_token,
    update_user_settings,
)
from knowledgenest.auth.schema import (
    SignupUserIn,
    SignupUserOut,
    TokenIn,
    UserSettings,
    UserOut,
)
from starlette.responses import Response

auth_router = APIRouter(prefix="/auth", tags=["authentication"])
users_router = APIRouter(prefix="/users", tags=["users"])


@auth_router.post("/login")
def login(db: DbSession, request: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(request.username, db)
    if not verify_hash(request.password, user.password):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bad credentials"
        )

    access_token, expiration_time = create_access_token(
        data={"username": request.username}
    )

    return {
        "access_token": access_token,
        "token-type": "bearer",
        "email": request.username,
        "token_expiration_time": expiration_time,
    }


@auth_router.post("/signup", response_model=SignupUserOut)
def signup(request: SignupUserIn, db: DbSession):
    new_user = create_user(request.email, request.password, db)
    return new_user


@auth_router.post("/verify")
def verify(request: TokenIn):
    if verify_access_token(request.token):
        return Response(status_code=HTTP_200_OK)
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Incorrect Token")


@users_router.put("/settings", response_model=UserSettings)
def update_settings(request: UserSettings, current_user: CurrentUser, db: DbSession):
    return update_user_settings(request.ai_provider, current_user.id, db)


@users_router.get("/me", response_model=UserOut)
def me(current_user: CurrentUser):
    return current_user
