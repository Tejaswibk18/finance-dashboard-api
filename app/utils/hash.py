import hashlib
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:

    @staticmethod
    def _pre_hash(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def hash_password(password: str):
        return pwd_context.hash(Hash._pre_hash(password))

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str):
        return pwd_context.verify(Hash._pre_hash(plain_password), hashed_password)