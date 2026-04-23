from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from crud.database import get_session
from schemas.user import UserCreate, UserRead
from sqlmodel import Session
from crud.users import get_user_by_email, create_user
from models.auth import Token
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from utils.security import create_access_token ,authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

router = APIRouter()


@router.post("/register/", response_model=UserRead)
async def register_user(
    background_tasks: BackgroundTasks,
    user_in: UserCreate,
    session: Session = Depends(get_session),
):
    # user = UserRead(id="123e4567-e89b-12d3-a456-426614174000", email=user_in.email)
    # verify that the user does not already exist
    user = get_user_by_email(session, user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # save the user to the database
    user = create_user(session, email=user_in.email, password=user_in.password)

    return user

@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session)
) -> Token:
    user = authenticate_user(session, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
