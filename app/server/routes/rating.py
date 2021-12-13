import logging
from typing import Any, List
from bson.objectid import ObjectId
from fastapi import APIRouter, Body, HTTPException, Response, status, logger
from fastapi.encoders import jsonable_encoder

from app.server.config.database import (
    create_many,
    delete,
    find_all,
    find_one,
    rating_validator,
    update,
)
from app.server.models.rating import (
    ErrorResponseModel,
    ResponseModel,
    RatingSchema,
    UpdateRatingModel,
)

router = APIRouter()

@router.post("/", response_description="Rating data added into the database", status_code=status.HTTP_201_CREATED)
async def createRating(response: Response, rating: List[RatingSchema] = Body(default=None)):
    if rating == None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseModel(status.HTTP_400_BAD_REQUEST, "Validation failed (parsable array expected)", "Bad Request")

    if len(rating) == 0:
        return rating
        
    rating = jsonable_encoder(rating)
    if (rating_validator(rating)):
        new_rating = await create_many(rating)
        if (new_rating):
            return ResponseModel(new_rating, "Rating added successfully.")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Toto1")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Toto2")

@router.get("/", response_description="Get all rating data", status_code=status.HTTP_200_OK)
async def findAllRating():
    rating = await find_all()
    return ResponseModel(rating, "All rating retrieved successfully.")

@router.get("/{id}", response_description="Get all rating data", status_code=status.HTTP_200_OK)
async def findOneRating(id : str):
    if (ObjectId.is_valid(id)):
        rating = await find_one(id)
        if rating:
            return ResponseModel(rating, "Rating retrieved successfully.")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

@router.put("/{id}", response_description="Update a rating", status_code=status.HTTP_200_OK)
async def updateOneRating(id: str, ratingUpdate: UpdateRatingModel = Body(...)):
    if (ObjectId.is_valid(id)):
        ratingUpdate = {k: v for k, v in ratingUpdate.dict().items() if v is not None}
        updateRating = await update(id, ratingUpdate)
        if updateRating:
            updatedRating = await find_one(id)
            return ResponseModel(updatedRating, "Rating updated successfully.")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")  
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")  

@router.delete("/{id}", response_description="Update a rating", status_code=status.HTTP_204_NO_CONTENT)
async def deleteOneRating(id: str):
    if (ObjectId.is_valid(id)):
        deleteRating = await delete(id)
        if (deleteRating):
            return ResponseModel(None, "Rating deleted successfully.")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")  
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")     
