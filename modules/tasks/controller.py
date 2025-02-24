from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from util.database import get_db
from modules.tasks.service import TaskService  
from modules.tasks.schema import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task for a user"""
    return TaskService.create_task(db, task)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: UUID, db: Session = Depends(get_db)):
    """Fetch a task by ID"""
    task = TaskService.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/user/{user_id}", response_model=list[TaskResponse])
def get_tasks_by_user(user_id: UUID, db: Session = Depends(get_db)):
    """Fetch all tasks for a specific user"""
    return TaskService.get_tasks_by_user(db, user_id)

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: UUID, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """Update an existing task"""
    updated_task = TaskService.update_task(db, task_id, task_update)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/{task_id}")
def delete_task(task_id: UUID, db: Session = Depends(get_db)):
    """Delete a task by ID"""
    result = TaskService.delete_task(db, task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result

@router.post("/create_task", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task for a user"""
    return TaskService.create_task(db, task)