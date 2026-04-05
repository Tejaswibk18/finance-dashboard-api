from fastapi import APIRouter, Depends, Query, HTTPException
from datetime import datetime
from typing import Optional

from fastapi.responses import JSONResponse
from app.schemas.record_schema import RecordCreate, RecordUpdate
from app.services.record_service import RecordService
from app.auth.dependencies import require_roles
from app.utils.response import ResponseHandler

router = APIRouter(prefix="/records", tags=["Records"])


#  Create (Admin only)
@router.post("/")
def create_record(
    record: RecordCreate,
    user=Depends(require_roles(["admin"]))
):
    try:

        record_data = RecordService.create_record(record, user)

        return ResponseHandler.success(
            message="Record created successfully",
            data=record_data
        )

    except HTTPException as e:
        return ResponseHandler.error(message=e.detail, status_code=e.status_code)


#  Get (All roles)
@router.get("/")
def get_records(
    type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    user=Depends(require_roles(["admin", "analyst", "viewer"]))
):
    try:
        filters = {
            "type": type,
            "category": category,
            "start_date": start_date
        }

        data = RecordService.get_records(filters, page, limit)

        return ResponseHandler.success(
            message="Records fetched",
            data=data
        )

    except HTTPException as e:
        return ResponseHandler.error(message=e.detail, status_code=e.status_code)


#  Update (Admin only)
@router.put("/{record_id}")
def update_record(
    record_id: str,
    record: RecordUpdate,
    user=Depends(require_roles(["admin"]))
):
    try:
        RecordService.update_record(record_id, record)

        return ResponseHandler.success(
            message="Record updated successfully"
        )

    except HTTPException as e:
        return ResponseHandler.error(message=e.detail, status_code=e.status_code)


#  Delete (Admin only)
@router.delete("/{record_id}")
def delete_record(record_id: str, user=Depends(require_roles(["admin"]))):
    try:
        RecordService.delete_record(record_id)

        return ResponseHandler.success(
            message="Record deleted successfully"
        )

    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,  # ✅ THIS FIXES YOUR ISSUE
            content=ResponseHandler.error(
                message=e.detail,
                status_code=e.status_code
            )
        )