from sqlmodel import SQLModel,Session, create_engine
from modules.users.model import User  # Ensure User model is imported
from modules.tasks.model import Task  # Ensure Task model is imported

database_url = "sqlite:///database.db"
engine = create_engine(database_url, connect_args={"check_same_thread": False})

# Function to create database and tables
def create_db_and_table():
    SQLModel.metadata.create_all(engine)  # Creates tables for User and Task

# ✅ Dependency function for database session
def get_db():
    db = Session(engine)  # Create a new session
    try:
        yield db  # Yield session to FastAPI routes
    finally:
        db.close()  # Close session after request
