from typing import Optional

from pydantic import BaseModel, Field

import datetime

class RatingSchema(BaseModel):
    product: str = Field(...)
    user: str = Field(...)
    score: float = Field(...)
    date: datetime.date = Field(...)


class UpdateRatingModel(BaseModel):
    product: Optional[str]
    user: Optional[str]
    score: Optional[float]
    date: Optional[datetime.date]

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(code, message, error):
    return {"statusCode":code, "message":message, "error":error}