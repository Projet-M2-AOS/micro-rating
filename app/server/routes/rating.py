from typing import List, Optional
from bson.objectid import ObjectId
from fastapi import Body, Response, status, logger
from fastapi.encoders import jsonable_encoder
from app.server.routes.router import APIRouter

from app.server.config.database import (
    create_many,
    delete,
    find_all,
    find_one,
    rating_validator,
    update,
)
from app.server.models.rating import (
    RatingSchema,
    UpdateRatingModel,
)

from app.server.models.response import ErrorResponseModel

router = APIRouter()

#HTTP [POST] Create new rating
@router.post("/", response_description="Rating data added into the database", status_code=status.HTTP_201_CREATED)
async def createRating(response: Response, rating: List[RatingSchema] = Body(default=None)):
    #Check for null body
    if rating == None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseModel(status.HTTP_400_BAD_REQUEST, "Validation failed (parsable array expected)", "Bad Request")
    #Check for empty array body
    if len(rating) == 0:
        return rating
    
    #Convert to JSON
    rating = jsonable_encoder(rating)
    #Check if JSON is valid
    if (rating_validator(rating)):
        new_rating = await create_many(rating)
        if (new_rating):
            for i in range(len(new_rating)):
                new_rating[i]["_id"] = new_rating[i].pop("id")
            return new_rating
        else:
            return ErrorResponseModel(status.HTTP_400_BAD_REQUEST, "Cannot insert new rating", "Bad Request")
    else:
        return ErrorResponseModel(status.HTTP_400_BAD_REQUEST, "Error while validating rating, product or user field is not ObjectID", "Bad Request")

#HTTP [GET] Get all ratings (or by query)
@router.get("/", response_description="Get all rating data", status_code=status.HTTP_200_OK)
async def findAllRating(userId : Optional[str] = None, productId : Optional[str] = None):
    ratings = await find_all(userId, productId)
    for i in range(len(ratings)):
        ratings[i]["_id"] = ratings[i].pop("id")
    return ratings

#HTTP [GET] Get one rating by id
@router.get("/{id}", response_description="Get all rating data", status_code=status.HTTP_200_OK)
async def findOneRating(response: Response, id : str):
    #Check if given id parameter is valid ObjectId (mongo standard)
    if (ObjectId.is_valid(id)):
        rating = await find_one(id)
        if rating:
            rating["_id"] = rating.pop("id") #Convert key "id" to "_id", make response more look like Nest.js
            return rating
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"statusCode":status.HTTP_404_NOT_FOUND, "message":"Not found"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseModel(status.HTTP_400_BAD_REQUEST, "Invalid ObjectId", "Bad Request")

#HTTP [PUT] Edit one rating by id
@router.put("/{id}", response_description="Update a rating", status_code=status.HTTP_200_OK)
async def updateOneRating(response: Response, id: str, ratingUpdate: UpdateRatingModel = Body(...)):
    #Check if given id parameter is valid ObjectId (mongo standard)
    if (ObjectId.is_valid(id)):
        ratingUpdate = {k: v for k, v in ratingUpdate.dict().items() if v is not None}
        updateRating = await update(id, ratingUpdate)
        if updateRating:
            updatedRating = await find_one(id)
            updatedRating["_id"] = updatedRating.pop("id") #Convert key "id" to "_id", make response more look like Nest.js
            return updatedRating
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"statusCode":status.HTTP_404_NOT_FOUND, "message":"Not found"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseModel(status.HTTP_400_BAD_REQUEST, "Invalid ObjectId", "Bad Request")

#HTTP [DELETE] Delete one rating by id
@router.delete("/{id}", response_description="Update a rating", status_code=status.HTTP_204_NO_CONTENT)
async def deleteOneRating(response: Response, id: str):
    #Check if given id parameter is valid ObjectId (mongo standard)
    if (ObjectId.is_valid(id)):
        deleteRating = await delete(id)
        if deleteRating:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"statusCode":status.HTTP_404_NOT_FOUND, "message":"Not found"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseModel(status.HTTP_400_BAD_REQUEST, "Invalid ObjectId", "Bad Request")    
