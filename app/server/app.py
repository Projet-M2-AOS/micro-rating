import logging
from fastapi import FastAPI, requests, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.server.routes.rating import router as RatingRouter

#FastAPI instance
app = FastAPI()

#Override validation exception handler, make error message on Schema validation to look like Nest.js standard
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: requests, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={'statusCode': status.HTTP_400_BAD_REQUEST, 'message': str(exc).split("\n"), "error":"Bad request"},
    )

#Use /ratings router
app.include_router(RatingRouter, tags=["micro-ratings"], prefix="/ratings")

#Swagger json endpoint
@app.get("/docs-json")
async def getOpenApi():
    return app.openapi()
