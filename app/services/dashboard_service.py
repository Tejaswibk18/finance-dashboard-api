from fastapi import HTTPException
from app.db.mongo import mongodb


class DashboardService:

    @staticmethod
    def get_summary():
        try:
            pipeline = [
                {"$match": {"is_deleted": False}},
                {
                    "$group": {
                        "_id": "$type",
                        "total": {"$sum": "$amount"}
                    }
                }
            ]

            result = list(mongodb.db.records.aggregate(pipeline))

            income = 0
            expense = 0

            for r in result:
                if r["_id"] == "income":
                    income = r["total"]
                elif r["_id"] == "expense":
                    expense = r["total"]

            return {
                "total_income": income,
                "total_expense": expense,
                "net_balance": income - expense
            }

        except Exception:
            raise HTTPException(status_code=500, detail="Failed to fetch summary")

    # MUST BE INSIDE CLASS (INDENTED)
    @staticmethod
    def category_breakdown():
        try:
            pipeline = [
                {"$match": {"is_deleted": False}},
                {
                    "$group": {
                        "_id": "$category",
                        "total": {"$sum": "$amount"}
                    }
                }
            ]

            result = list(mongodb.db.records.aggregate(pipeline))

            return [
                {
                    "category": r["_id"],
                    "total": r["total"]
                }
                for r in result
            ]

        except Exception:
            raise HTTPException(status_code=500, detail="Failed to fetch category data")

    # ALSO INSIDE CLASS
    @staticmethod
    def recent_activity():
        try:
            records = list(
                mongodb.db.records.find({"is_deleted": False})
                .sort("date", -1)
                .limit(5)
            )

            for r in records:
                r["_id"] = str(r["_id"])

            return records

        except Exception:
            raise HTTPException(status_code=500, detail="Failed to fetch recent activity")
        
    @staticmethod
    def get_trends(group_by: str):
        try:
            if group_by not in ["monthly", "weekly"]:
                raise HTTPException(status_code=400, detail="Invalid group_by value")

            if group_by == "monthly":
                group_id = {
                    "year": {"$year": "$date"},
                    "month": {"$month": "$date"}
                }
            else:
                group_id = {
                    "year": {"$year": "$date"},
                    "week": {"$isoWeek": "$date"}
                }

            pipeline = [
                {
                    "$match": {
                        "is_deleted": False,
                        "date": {"$type": "date"}
                    }
                },
                {
                    "$group": {
                        "_id": group_id,
                        "total": {"$sum": "$amount"}
                    }
                },
                {
                    "$sort": {
                        "_id.year": 1,
                        **({"_id.month": 1} if group_by == "monthly" else {"_id.week": 1})
                    }
                }
            ]

            result = list(mongodb.db.records.aggregate(pipeline))

            formatted = []

            for r in result:
                if group_by == "monthly":
                    label = f"{r['_id']['year']}-{r['_id']['month']:02d}"
                else:
                    label = f"{r['_id']['year']}-W{r['_id']['week']}"

                formatted.append({
                    "period": label,
                    "total": r["total"]
                })

            return formatted

        except HTTPException as e:
            raise e
        except Exception as e:
            print("ERROR:", e)  # debug
            raise HTTPException(status_code=500, detail="Failed to fetch trends")