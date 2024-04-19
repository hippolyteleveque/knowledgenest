from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from .service import create_access_token, verify_access_token
from .schema import SignupUserIn, SignupUserOut, TokenIn
from starlette.responses import Response

router = APIRouter(prefix="/auth", tags=["authentication"])

users = []


@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends()):
    user_emails = [el[0] for el in users]
    try:
        user_idx = user_emails.index(request.username)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Username {request.username} does not exist",
        )
    if not request.password == users[user_idx][1]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password"
        )

    access_token = create_access_token(data={"username": request.username})

    return {
        "access_token": access_token,
        "token-type": "bearer",
        "user_id": 1,
        "email": request.username,
    }


@router.post("/signup", response_model=SignupUserOut)
def signup(request: SignupUserIn):
    users.append((request.email, request.password))
    return request


@router.post("/verify")
def verify(request: TokenIn):
    print(request)
    if verify_access_token(request.token):
        return Response(status_code=HTTP_200_OK)
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Incorrect Token")
