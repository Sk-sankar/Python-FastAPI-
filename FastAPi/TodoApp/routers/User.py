from fastapi import APIRouter, Depends,HTTPException,Path
from starlette import status
from models import Todos,Users
from sqlalchemy.orm import Session
from database import  SessionLocal
from schema import TodoRequest,userverfication
from typing import Annotated  
from .auth import get_Current_user
from passlib.context import CryptContext


app = APIRouter(prefix="/User",tags=["User"])



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency=Annotated[Session, Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_Current_user)]
bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated="auto")






@app.get("/",status_code=status.HTTP_202_ACCEPTED)

async def get_user(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail="authentication failed")
    return db.query(Users).filter(Users.id==user.get("id")).first()


@app.put("/password",status_code=status.HTTP_204_NO_CONTENT)

async def update_password(user:user_dependency,db:db_dependency,user_verify:userverfication):
    if user is None :
        raise HTTPException(status_code=401,detail="authentication failed")
    user_pass=db.query(Users).filter(Users.id==user.get("id")).first()
    
    if not bcrypt_context.verify(user_verify.password,user_pass.hash_password):
        raise HTTPException(status_code=401,detail="error on password change")
    
    user_pass.hash_password=bcrypt_context.hash(user_verify.new_password)
    db.add(user_pass)
    db.commit()