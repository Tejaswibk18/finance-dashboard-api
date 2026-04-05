from bson import ObjectId
from fastapi import HTTPException


class Helper:

    @staticmethod
    def validate_object_id(id: str):
        if not ObjectId.is_valid(id):
            raise HTTPException(
                status_code=400,
                detail="Invalid record ID format"
            )
        return ObjectId(id)