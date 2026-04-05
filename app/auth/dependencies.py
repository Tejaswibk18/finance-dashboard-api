from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.jwt_handler import JWTHandler
from app.db.mongo import mongodb
from bson import ObjectId

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        token = credentials.credentials
        payload = JWTHandler.decode_token(token)

        user = mongodb.db.users.find_one({
            "_id": ObjectId(payload["user_id"])
            })
        

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        if not user.get("is_active"):
            raise HTTPException(status_code=403, detail="User inactive")

        return user

    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    

def require_roles(allowed_roles: list):
    
    def role_checker(user=Depends(get_current_user)):
        if user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )
        return user

    return role_checker