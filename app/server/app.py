import logging
from fastapi import FastAPI, requests, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.server.routes.rating import router as RatingRouter

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: requests, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={'statusCode': status.HTTP_400_BAD_REQUEST, 'message': str(exc).split("\n"), "error":"Bad request"},
    )

app.include_router(RatingRouter, tags=["Ratings"], prefix="/ratings")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}

@app.get("/docs-json")
async def getOpenApi():
    return app.openapi()
