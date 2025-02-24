from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime, timezone

def generate_timestamp():
    return datetime.now(timezone.utc)

class UserBase(SQLModel):
    fullName: str = Field(min_length=3)
    email: str = Field(unique=True, min_length=3)

class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=generate_timestamp)
    updated_at: datetime = Field(default_factory=generate_timestamp)

    tasks: list["Task"] = Relationship(back_populates="user")
