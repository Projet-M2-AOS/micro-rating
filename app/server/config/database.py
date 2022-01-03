from typing import List
import motor.motor_asyncio
from dotenv import load_dotenv
import os

from bson.objectid import ObjectId

#Load env variables
load_dotenv()

#Define MONGO database connection string
MONGO_URL = os.environ.get("MONGO_URL")

#Define new client
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)

#Set database
database = client.ratings

ratings_collection = database.get_collection("ratings")

#Convert JSON to Python dict
def rating_deserializer(rating) -> dict:
    return {
        "id": str(rating["_id"]),
        "product": rating["product"],
        "user": rating["user"],
        "score": rating["score"],
        "date": rating["date"],
    }

#Allow to validate if product and user are ObjectID for a Rating ressource
def rating_validator(rating) -> bool:
    result = True
    for r in rating:
        if not ObjectId.is_valid(r["product"]) and not ObjectId.is_valid(r["user"]):
            return False
    return result
   
#Find all ratings in Database, if userId or productId is not None use it for query
async def find_all(userId, productId):
    ratings = []
    query = {}
    #Case when ratings are query by user and by product
    if userId and productId:
        query = {'$and': [
            {'user':{'$eq':userId}},
            {'product':{'$eq':productId}}
        ]}
    #Case when ratings are query by user
    elif userId:
        query = {'user':{'$eq':userId}}
    #Case when ratings are query by product
    elif productId:
        query = {'product':{'$eq':productId}}
    
    #Retrieve ratings that match from database
    async for rating in ratings_collection.find(query):
        ratings.append(rating_deserializer(rating))
    return ratings

#Find one ratings by id
async def find_one(id: str) -> dict:
    rating = await ratings_collection.find_one(
        {"_id": ObjectId(id)}
    )
    if rating:
        return rating_deserializer(rating)

#Create many ratings
async def create_many(rating_data: List[dict]) -> List[dict]:
    rating = await ratings_collection.insert_many(rating_data)
    new_rating = []
    async for r in ratings_collection.find({"_id": {"$in": rating.inserted_ids}}):
        new_rating.append(rating_deserializer(r))
    return new_rating

#Update one rating
async def update(id: str, data: dict):
    if len(data) < 1:
        return False
    if "date" in data:
        data["date"] = data["date"].strftime('%Y-%m-%d')

    rating = await ratings_collection.find_one(
        {"_id":ObjectId(id)}
    )
    if rating:
        updated_rating = await ratings_collection.update_one(
            {"_id":ObjectId(id)}, {"$set":data}
        )
        if updated_rating:
            return True
    return False

#Delete one rating
async def delete(id: str):
    rating = await ratings_collection.find_one(
        {"_id":ObjectId(id)}
    )
    if rating:
        await ratings_collection.delete_one(
            {"_id":ObjectId(id)}    
        )
        return True
    return False