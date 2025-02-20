from fastapi import APIRouter,HTTPException, Depends
from .service import UserService
from .model import User
from .schema import UserCreate, UserResponse
router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[User])
def get_users():
    return UserService.get_users()


@router.get("/{user_id}", response_model=UserResponse)
def read(user_id: int):
    user = UserService.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserResponse) 
def create(user: UserCreate):
    return UserService.create_user(user)

@router.put("/{user_id}", response_model=UserResponse)
def update(user_id: int, user: UserCreate):
    result = UserService.update_user(user_id, user)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result

@router.delete("/{user_id}")
def delete(user_id: int):
    result = UserService.delete_user(user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result

