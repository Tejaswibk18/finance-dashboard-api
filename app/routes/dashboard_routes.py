from fastapi import APIRouter, Depends, HTTPException
from app.services.dashboard_service import DashboardService
from app.auth.dependencies import require_roles
from app.utils.response import ResponseHandler
from fastapi import Query

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# Summary (Analyst + Admin)
@router.get("/summary")
def get_summary(user=Depends(require_roles(["admin", "analyst"]))):
    try:
        data = DashboardService.get_summary()

        return ResponseHandler.success(
            message="Dashboard summary fetched",
            data=data
        )

    except HTTPException as e:
        return ResponseHandler.error(
            message=e.detail,
            status_code=e.status_code
        )


#  Category Breakdown
@router.get("/category")
def category_data(user=Depends(require_roles(["admin", "analyst"]))):
    try:
        data = DashboardService.category_breakdown()

        return ResponseHandler.success(
            message="Category breakdown fetched",
            data=data
        )

    except HTTPException as e:
        return ResponseHandler.error(
            message=e.detail,
            status_code=e.status_code
        )


@router.get("/trends")
def get_trends(
    group_by: str = Query(..., description="monthly or weekly"),
    user=Depends(require_roles(["admin", "analyst"]))):
    try:
        data = DashboardService.get_trends(group_by)

        return ResponseHandler.success(
            message=f"{group_by.capitalize()} trends fetched",
            data=data
        )

    except HTTPException as e:
        return ResponseHandler.error(
            message=e.detail,
            status_code=e.status_code
        )

#  Recent Activity
@router.get("/recent")
def recent_activity(user=Depends(require_roles(["admin", "analyst"]))):
    try:
        data = DashboardService.recent_activity()

        return ResponseHandler.success(
            message="Recent activity fetched",
            data=data
        )

    except HTTPException as e:
        return ResponseHandler.error(
            message=e.detail,
            status_code=e.status_code
        )