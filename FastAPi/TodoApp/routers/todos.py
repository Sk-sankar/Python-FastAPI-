from fastapi import APIRouter, Depends,HTTPException,Path
from starlette import status
from models import Todos
from sqlalchemy.orm import Session
from database import  SessionLocal
from schema import TodoRequest
from typing import Annotated  
from .auth import get_Current_user


app = APIRouter()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency=Annotated[Session, Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_Current_user)]
        
@app.get("/todos")
async def read_all(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail="authentication failed")
    return db.query(Todos).filter(Todos.Owner_id==user.get("id")).all()



@app.get("/todos/{todo_id}",status_code=status.HTTP_200_OK)
async def read_todo(user:user_dependency,db:db_dependency,todo_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail="authentication failed")
    todo_model=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.Owner_id==user.get("id")).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404,detail="todo is not found")



@app.post("/todo",status_code=status.HTTP_201_CREATED)
async def create_todo(user:user_dependency,db:db_dependency,todo_request:TodoRequest):
    
    if user is None:
        raise HTTPException(status_code=401,detail="authentication failed")
    
    todo_model = Todos(**todo_request.model_dump(), Owner_id=user.get("id"))
    
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model


@app.put("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user:user_dependency,db:db_dependency,todo_request:TodoRequest,todo_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail="authentication failed")
    
    todo_model=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.Owner_id==user.get("id")).first()
    if todo_model is  None:
        raise HTTPException(status_code=404,detail="todo not found")
    
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model
    
    
@app.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependency,db:db_dependency,todo_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail="authentication failed")
    
    todo_model=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.Owner_id==user.get("id")).first()
    if todo_model is None:
         raise HTTPException(status_code=404,detail="todo not found")
        
    db.query(Todos).filter(Todos.id==todo_id).filter(Todos.Owner_id==user.get("id")).delete()
    
    db.commit()