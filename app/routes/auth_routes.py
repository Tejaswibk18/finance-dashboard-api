from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserCreate, UserLogin
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.utils.response import ResponseHandler

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(user: UserCreate):
    try:
        user_id = UserService.create_user(user)
        return ResponseHandler.success(
            message="User registered successfully",
            data={"user_id": user_id}
        )
    except HTTPException as e:
        return ResponseHandler.error(
            message=e.detail,
            status_code=e.status_code
        )


@router.post("/login")
def login(user: UserLogin):
    try:
        token = AuthService.login(user)
        return ResponseHandler.success(
            message="Login successful",
            data={"access_token": token}
        )
    except HTTPException as e:
        return ResponseHandler.error(
            message=e.detail,
            status_code=e.status_code
        )