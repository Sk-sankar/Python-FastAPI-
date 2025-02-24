from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone

def generate_time_stamp():
    return datetime.now(timezone.utc)

# Base Schema for Task
class TaskBase(SQLModel):
    title: str = Field(min_length=3, max_length=100)
    description: str | None = None
    completed: bool = Field(default=False)

# Schema for Creating a Task
class TaskCreate(TaskBase):
    user_id: UUID  # Foreign key linking Task to User

# Schema for Updating a Task
class TaskUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None

# Schema for Response (Read Task)
class TaskResponse(TaskBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
