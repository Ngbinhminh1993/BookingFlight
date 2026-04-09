from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from crud.database import get_session
from schemas.user import UserCreate, UserRead
from sqlmodel import Session
from crud.users import get_user_by_email, create_user

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
