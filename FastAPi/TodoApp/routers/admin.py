from fastapi import APIRouter, Depends,HTTPException,Path
from starlette import status
from models import Todos
from sqlalchemy.orm import Session
from database import  SessionLocal
from schema import TodoRequest
from typing import Annotated  
from .auth import get_Current_user


app = APIRouter(prefix="/admin",tags=["admmin"])



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency=Annotated[Session, Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_Current_user)]
        
        
        
        
        
        
@app.get("/todo",status_code=status.HTTP_200_OK)

async def read_all(user:user_dependency,db:db_dependency):
    if user is None or user.get("role")!="admin":
        raise HTTPException(status_code=401,detail="authentication failed")
    
    return db.query(Todos).all()

@app.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)

async def delete_todo(user:user_dependency,db:db_dependency,todo_id:int= Path(gt=0)):
    if user is None or user.get("role")!="admin":
        raise HTTPException(status_code=401,detail="authentication failed")
    todo=db.query(Todos).filter(Todos.id==todo_id).first()
    if todo is None :
        raise HTTPException(status_code=404,detail="todo not found")
    db.query(Todos).filter(Todos.id==todo_id).delete()
    db.commit()    
