    
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from database import Base

class Users(Base):
    __tablename__="Users"
    
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,unique=True)
    username=Column(String,unique=True)
    first_name=Column(String)
    lastname=Column(String)
    hash_password=Column(String)
    is_active=Column(Boolean,default=True)
    role=Column(String)
       
    

class Todos(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)  # ✅ Correct: 'Column' (uppercase C)
    title = Column(String, index=True)
    description=Column(String)
    priority=Column(Integer)
    complete = Column(Boolean, default=False)
    Owner_id=Column(Integer,ForeignKey("Users.id"))