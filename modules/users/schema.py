from pydantic import BaseModel
from uuid import UUID

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(UserCreate):
    id: UUID

    class Config:
        from_attributes = True
