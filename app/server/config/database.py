from typing import List
import motor.motor_asyncio
from dotenv import load_dotenv
import os

from bson.objectid import ObjectId

load_dotenv()

MONGO_URL = os.environ.get("MONGO_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)

database = client.ratings

ratings_collection = database.get_collection("ratings")

def rating_deserializer(rating) -> dict:
    return {
        "id": str(rating["_id"]),
        "product": rating["product"],
        "user": rating["user"],
        "score": rating["score"],
        "date": rating["date"],
    }

def rating_validator(rating) -> bool:
    result = True
    for r in rating:
        if not ObjectId.is_valid(r["product"]) and not ObjectId.is_valid(r["user"]) and not ObjectId.is_valid(r["score"]):
            return False
    return result
   
async def find_all():
    ratings = []
    async for rating in ratings_collection.find():
        ratings.append(rating_deserializer(rating))
    return ratings

async def find_one(id: str) -> dict:
    rating = await ratings_collection.find_one(
        {"_id": ObjectId(id)}
    )
    if rating:
        return rating_deserializer(rating)

async def create_many(rating_data: List[dict]) -> List[dict]:
    rating = await ratings_collection.insert_many(rating_data)
    new_rating = []
    async for r in ratings_collection.find({"_id": {"$in": rating.inserted_ids}}):
        new_rating.append(rating_deserializer(r))
    print(new_rating)
    return new_rating

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