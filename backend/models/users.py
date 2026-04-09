# models/users.py
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4


class UserInDB(SQLModel, table=True):  # ← Add table=True!
    __tablename__ = "userindb"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    password: str
