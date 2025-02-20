# This file contains the model for the user table in the database
# It also contains the base model for the user table
from sqlmodel import SQLModel,Field
from uuid import UUID ,uuid4
from datetime import datetime,timezone

def generate_time_stamp():
    return datetime.now(timezone.utc)

class UserBase(SQLModel):
    fullName:str=Field(min_length=3)
    email:str=Field(unique=True,min_length=3)
    
class User(UserBase,table=True):
    id:UUID=Field(primary_key=True,default_factory=uuid4)
    created_at:datetime=Field(default_factory=generate_time_stamp)
    updated_at:datetime=Field(default_factory=generate_time_stamp)
    
    
__all__ = [User,UserBase]
    