from fastapi import APIRouter, Depends
from app.auth.dependencies import require_roles

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
def get_users(user=Depends(require_roles(["admin"]))):
    return {"message": "Only admin can see this"}