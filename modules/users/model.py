from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime, timezone
from util.database import engine
from sqlmodel import Session,select 
from modules.users.schema import UserCreate

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


class userDAO:
     def get_users():
        with Session(engine) as session:
            users=session.exec(select(User)).all()
        return users


     def create_user(user:UserCreate):
        with Session(engine) as session:
            db_user=User(fullName=user.name,email=user.email)
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
        return db_user
    
     def update_user(user_id:int,user:UserCreate):
        with Session(engine) as session:
            db_user=session.get(User,user_id)
            db_user.fullName=user.name
            db_user.email=user.email
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
        return db_user
    
     def delete_user(user_id:int):           
        with Session(engine) as session:
            user=session.get(User,user_id)
            session.delete(user)
            session.commit()
        return {"message":"User deleted successfully"}
 
