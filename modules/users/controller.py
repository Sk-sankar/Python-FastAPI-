from fastapi import APIRouter
from .service import UserService
from .schema import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[User])
def get_users():
    return UserService.get_users()

