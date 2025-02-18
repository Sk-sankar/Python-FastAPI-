from contextlib import asynccontextmanager
from fastapi import FastAPI
from modules.users.controller import router as users_router
from util.database import create_db_and_table

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_table()
    yield
    
app = FastAPI(lifespan=lifespan)

# Include the users router
app.include_router(users_router)

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI Users API"}
