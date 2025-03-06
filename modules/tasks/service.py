from sqlmodel import Session, select
from uuid import UUID
from modules.tasks.model import Task
from modules.tasks.schema import TaskCreate, TaskUpdate

class TaskService:
    
    @staticmethod
    def create_task(db: Session, task_data: TaskCreate):
        task = Task(**task_data.dict())
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def get_task(db: Session, task_id: UUID):
        return db.exec(select(Task).where(Task.id == task_id)).first()

    @staticmethod
    def get_tasks_by_user(db: Session, user_id: UUID):

        return db.exec(select(Task).where(Task.user_id == user_id)).all()

    @staticmethod
    def update_task(db: Session, task_id: UUID, task_update: TaskUpdate):
        task = db.exec(select(Task).where(Task.id == task_id)).first()
        if not task:
            return None
        task_data = task_update.dict(exclude_unset=True)
        for key, value in task_data.items():
            setattr(task, key, value)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def delete_task(db: Session, task_id: UUID):
        """Delete a task by ID"""
        task = db.exec(select(Task).where(Task.id == task_id)).first()
        if not task:
            return None
        db.delete(task)
        db.commit()
        return {"message": "Task deleted successfully"}
