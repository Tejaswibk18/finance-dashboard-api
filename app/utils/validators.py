import re
from fastapi import HTTPException


class Validator:

    @staticmethod
    def validate_password(password: str):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,}$"

        if not re.match(pattern, password):
            raise HTTPException(
                status_code=400,
                detail="Password must be at least 8 characters long and include uppercase, lowercase, and special character"
            )