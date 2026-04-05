from jose import jwt , JWTError
from datetime import datetime, timedelta , timezone
from app.core.config import settings


class JWTHandler:

    @staticmethod
    def create_token(data: dict):

        payload = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        payload.update({"exp": expire})

        return jwt.encode(
            payload,
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )

    @staticmethod
    def decode_token(token: str):
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except JWTError:
            raise Exception("Invalid or expired token")