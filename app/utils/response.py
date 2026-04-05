from typing import Any


class ResponseHandler:

    @staticmethod
    def success(message: str = "Success", data: Any = None, status_code: int = 200):
        return {
            "status": "success",
            "message": message,
            "status_code": status_code,
            "data": data if data is not None else []
        }

    @staticmethod
    def error(message: str = "Something went wrong", data: Any = None, status_code: int = 400):
        return {
            "status": "failed",
            "message": message,
            "status_code": status_code,
            "data": data if data is not None else []
        }