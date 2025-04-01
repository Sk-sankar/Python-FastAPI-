from fastapi import FastAPI, Depends,HTTPException,Path
import models
from database import engine
from routers import auth,todos,admin,User

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.app)
app.include_router(todos.app)
app.include_router(admin.app)
app.include_router(User.app)
