from typing import Optional

from pydantic import BaseModel, Field

import datetime

#Rating Schema to create ressource
class RatingSchema(BaseModel):
    product: str = Field(...)
    user: str = Field(...)
    score: float = Field(...)
    date: datetime.date = Field(...)

#Rating Schema to update ressource
class UpdateRatingModel(BaseModel):
    product: Optional[str]
    user: Optional[str]
    score: Optional[float]
    date: Optional[datetime.date]