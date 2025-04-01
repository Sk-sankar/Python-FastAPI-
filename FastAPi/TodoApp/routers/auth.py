from fastapi import APIRouter,Depends,HTTPException
from schema import createUserRequest,token
from models import Users
from passlib.context import CryptContext # type: ignore
from sqlalchemy.orm import Session
from database import  SessionLocal
from typing import Annotated 
from starlette import status
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from datetime import timedelta,datetime,timezone

app=APIRouter(prefix="/auth",tags=["auth"])

secret_key='a3f5c7d8e4b913f8a2c57f3b7d9e6a4c123f98b67e5c1d8f0a3b7c9d2e4f8a6b'
alogo="HS256"


bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated="auto")

oauth2_bearer=OAuth2PasswordBearer(tokenUrl="auth/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency=Annotated[Session, Depends(get_db)]


def authenticate_user(username:str,password:str,db):
    user=db.query(Users).filter(Users.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hash_password):
        return False
    return user


 


def create_access_token(username:str,user_id:int,role:str,expires:timedelta):
    encode={"sub":username,"id":user_id,"role":role}
    expires=datetime.now(timezone.utc)+expires
    encode.update({"exp":expires})
    return jwt.encode(encode,secret_key,algorithm=alogo)
    

async def get_Current_user(token:Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload=jwt.decode(token,secret_key,algorithms=[alogo])
        username:str = payload.get("sub")
        user_id:int=payload.get("id")
        user_role:str=payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return {"user":username,"id":user_id,"role":user_role}
    except JWTError:
             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        
        


@app.post("/auth",status_code=status.HTTP_201_CREATED)

async def create_user(db:db_dependency,
                      create_user_request:createUserRequest):
    create_user_model=Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        lastname=create_user_request.last_name,
        role=create_user_request.role,
        hash_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
        
    )
    
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    
    
@app.post("/token",response_model=token)

async def login_for_acces_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    
    user=authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    
    token=create_access_token(user.username,user.id,user.role,timedelta(minutes=20))
    
    return {"access_token":token,"token_type":"bearer"}
        
