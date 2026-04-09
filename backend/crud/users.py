from sqlmodel import Session, select

from models.users import UserInDB
from utils.security import hash_password


def get_user_by_email(session: Session, email: str):
    # This is a placeholder function. In a real application, you would query the database.

    return session.exec(select(UserInDB).where(UserInDB.email == email)).first()


def create_user(session: Session, email: str, password: str):
    # This is a placeholder function. In a real application, you would hash the password and save the user to the database.
    hashed_password = hash_password(password)
    user = UserInDB(email=email, password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
