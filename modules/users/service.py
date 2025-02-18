from .model import user
from sqlmodel import select
from util.database import Session,engine
class UserService:
    def get_users():
        
        with Session(engine)as session:
            users=session.exec(select(user)).all()
        return users

 