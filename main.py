from fastapi import FastAPI
from contextlib import asynccontextmanager
from util.database import create_db_and_table
from modules.users.controller import router as users_router
from modules.tasks.controller import router as tasks_router
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_table()  # ✅ Ensure database is created
    yield

app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(users_router)
app.include_router(tasks_router)

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI Users API"}



