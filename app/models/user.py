from sqlmodel import Field, Relationship, SQLModel
from typing import Optional
from pydantic import EmailStr


class UserBase(SQLModel,):
    name: str = ""
    username: str = Field(index=True, unique=True)
    email: EmailStr = Field(index=True, unique=True)
    password: str
    role:str = ""

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    researcher: Optional["Researcher"] = Relationship(back_populates="user")
    admin: Optional["Admin"] = Relationship(back_populates="user")