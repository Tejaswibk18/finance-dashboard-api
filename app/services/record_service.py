from fastapi import HTTPException
from app.db.mongo import mongodb
from app.utils.helpers import Helper


class RecordService:

    @staticmethod
    def create_record(data, user):
        try:
            record = data.model_dump(mode="json")
            record["created_by"] = str(user["_id"])
            record["is_deleted"] = False

            result = mongodb.db.records.insert_one(record)

            record["_id"] = str(result.inserted_id)

            return record

        except Exception:
            raise HTTPException(status_code=500, detail="Record creation failed")

    @staticmethod
    def get_records(filters: dict, page: int, limit: int):
        try:
            query = {"is_deleted": False}

            if filters.get("type"):
                query["type"] = {
                    "$regex": f"^{filters['type']}$",
                    "$options": "i"
                }

            if filters.get("category"):
                query["category"] = {
                    "$regex": f"^{filters['category']}$",
                    "$options": "i"
                }

            if filters.get("start_date"):
                query["date"] = {"$gte": filters["start_date"]}

            skip = (page - 1) * limit

            cursor = mongodb.db.records.find(query).skip(skip).limit(limit)
            records = list(cursor)

            total_count = mongodb.db.records.count_documents(query)

            if not records:
                raise HTTPException(
                    status_code=404,
                    detail="No records found for given filters"
                )

            for r in records:
                r["_id"] = str(r["_id"])

            return {
                "items": records,
                "pagination": {
                    "total": total_count,
                    "page": page,
                    "limit": limit,
                    "pages": (total_count + limit - 1) // limit
                }
            }

        except HTTPException as e:
            raise e
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to fetch records")

    @staticmethod
    def update_record(record_id: str, data):
        try:
            obj_id = Helper.validate_object_id(record_id)

            update_data = {k: v for k, v in data.model_dump().items() if v is not None}

            result = mongodb.db.records.update_one(
                {"_id": obj_id, "is_deleted": False},  # ✅ important
                {"$set": update_data}
            )

            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Record not found or deleted")

            return True

        except HTTPException as e:
            raise e
        except Exception:
            raise HTTPException(status_code=500, detail="Update failed")

    @staticmethod
    def delete_record(record_id: str):
        try:
            obj_id = Helper.validate_object_id(record_id)

            result = mongodb.db.records.update_one(
                {"_id": obj_id, "is_deleted": False},
                {"$set": {"is_deleted": True}}
            )

            if result.matched_count == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Record not found or already deleted"
                )

            return True

        except HTTPException as e:
            raise e  
        except Exception:
            raise HTTPException(status_code=500, detail="Delete failed")