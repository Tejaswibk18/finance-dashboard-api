from fastapi import FastAPI
from app.routes import auth_routes, record_routes
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.utils.response import ResponseHandler
from app.routes import dashboard_routes


app = FastAPI(title="Finance Dashboard API")

app.include_router(auth_routes.router)
app.include_router(auth_routes.router)
app.include_router(record_routes.router)
app.include_router(dashboard_routes.router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):

    msg = exc.errors()[0].get("msg")

    if "Input should be" in msg:
        msg = "Role must be admin, analyst or viewer"

    return JSONResponse(
        status_code=400,
        content=ResponseHandler.error(
            message=msg,
            status_code=400
        )
    )