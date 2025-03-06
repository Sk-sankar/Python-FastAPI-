from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime, timezone
from modules.users.model import User  # Ensure correct import of User model

def generate_timestamp():
    return datetime.now(timezone.utc)

class TaskBase(SQLModel):
    title: str = Field(min_length=3)
    description: str = Field(default=None)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")  # Linking Task to User
    created_at: datetime = Field(default_factory=generate_timestamp)
    updated_at: datetime = Field(default_factory=generate_timestamp)

    user: User = Relationship(back_populates="tasks")
    
    