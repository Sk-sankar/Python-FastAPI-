from .model import User
from sqlmodel import select,Session
from util.database import engine
from .schema import UserCreate

class UserService:
    def get_users():
        with Session(engine) as session:
            users=session.exec(select(User)).all()
        return users


    def get_user(user_id:int):
        with Session(engine) as session:
            user=session.get(User,user_id)  
        return user

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