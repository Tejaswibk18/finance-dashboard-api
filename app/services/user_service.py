from fastapi import HTTPException
from app.db.mongo import mongodb
from app.utils.hash import Hash
from app.utils.validators import Validator


class UserService:

    @staticmethod
    def create_user(user_data):
        try:
            existing_user = mongodb.db.users.find_one({"email": user_data.email})
            if existing_user:
                raise HTTPException(
                    status_code=400,
                    detail="User already exists"
                )

            Validator.validate_password(user_data.password)

            user_dict = user_data.model_dump()
            user_dict["password"] = Hash.hash_password(user_dict["password"])
            user_dict["is_active"] = True

            result = mongodb.db.users.insert_one(user_dict)

            return str(result.inserted_id)

        except HTTPException as http_err:
            raise http_err
        except Exception:
            raise HTTPException(status_code=500, detail="User creation failed")