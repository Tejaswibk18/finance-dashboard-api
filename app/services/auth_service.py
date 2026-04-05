from fastapi import HTTPException
from app.db.mongo import mongodb
from app.utils.hash import Hash
from app.auth.jwt_handler import JWTHandler


class AuthService:

    @staticmethod
    def login(user_data):
        try:
            user = mongodb.db.users.find_one({"email": user_data.email})
            if not user:
                raise HTTPException(status_code=400, detail="Invalid credentials")

            if not Hash.verify_password(user_data.password, user["password"]):
                raise HTTPException(status_code=400, detail="Invalid credentials")

            token = JWTHandler.create_token({
                "user_id": str(user["_id"]),
                "role": user["role"]
            })

            return token

        except HTTPException as http_err:
            raise http_err
        except Exception:
            raise HTTPException(status_code=500, detail="Login failed")