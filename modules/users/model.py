# users = [
#     {"id": 1, "name": "Sankar", "email": "sankar@example.com", "age": 18},
#     {"id": 2, "name": "John", "email": "john@example.com", "age": 25},
#     {"id": 3, "name": "Priya", "email": "priya@example.com", "age": 22},
#     {"id": 4, "name": "Kumar", "email": "kumar@example.com", "age": 30},
#     {"id": 5, "name": "Meena", "email": "meena@example.com", "age": 28},
# ]
from sqlmodel import SQLModel,Field
from uuid import UUID ,uuid4
from datetime import datetime,timezone

def generate_time_stamp():
    return datetime.now(timezone.utc)

class UserBase(SQLModel):
    fullName:str=Field(min_length=3)
    email:str=Field(unique=True,min_length=3)
    
class user(UserBase,table=True):
    id:UUID=Field(primary_key=True,default_factory=uuid4)
    created_at:datetime=Field(default_factory=generate_time_stamp)
    updated_at:datetime=Field(default_factory=generate_time_stamp)
    
    
__all__ = [user,UserBase]
    