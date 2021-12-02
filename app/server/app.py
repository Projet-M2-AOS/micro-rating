from fastapi import FastAPI
from app.server.routes.rating import router as RatingRouter

app = FastAPI()

app.include_router(RatingRouter, tags=["Rating"], prefix="/rating")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
