from fastapi import APIRouter
from schema import createUserRequest
from models import Users

app=APIRouter()

@app.post("/auth/")

async def create_user(create_user_request:createUserRequest):
    create_user_model=Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        lastname=create_user_request.last_name,
        role=create_user_request.role,
        hash_password=create_user_request.password,
        is_active=True
        
    )
    
    
    return create_user_model
    