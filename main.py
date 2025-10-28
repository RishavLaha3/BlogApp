from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from models import BlogPost, UpdateBlogPost

app = FastAPI(title="Simple Blog API")

MONGO_URL = "mongodb+srv://ClimaticScholar:build7600@cluster0.0lsdnuv.mongodb.net/?appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URL)
db = client.blog_database
posts_collection = db.posts


def post_helper(post) -> dict:
    return {
        "id": str(post["_id"]),
        "title": post["title"],
        "content": post["content"],
        "author": post["author"],
        "created_at": post["created_at"]
    }



@app.post("/posts")
async def create_post(post: BlogPost):
    new_post = await posts_collection.insert_one(post.dict())
    created_post = await posts_collection.find_one({"_id": new_post.inserted_id})
    return post_helper(created_post)



@app.get("/posts")
async def get_all_posts():
    posts = []
    async for post in posts_collection.find():
        posts.append(post_helper(post))
    return posts



@app.get("/posts/{post_id}")
async def get_post(post_id: str):
    post = await posts_collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post_helper(post)



@app.put("/posts/{post_id}")
async def update_post(post_id: str, post_data: UpdateBlogPost):
    update_dict = {k: v for k, v in post_data.dict().items() if v is not None}
    if not update_dict:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = await posts_collection.update_one({"_id": ObjectId(post_id)}, {"$set": update_dict})
    if result.modified_count == 1:
        updated_post = await posts_collection.find_one({"_id": ObjectId(post_id)})
        return post_helper(updated_post)
    post = await posts_collection.find_one({"_id": ObjectId(post_id)})
    if post:
        return post_helper(post)
    raise HTTPException(status_code=404, detail="Post not found")



@app.delete("/posts/{post_id}")
async def delete_post(post_id: str):
    result = await posts_collection.delete_one({"_id": ObjectId(post_id)})
    if result.deleted_count == 1:
        return {"message": "Post deleted successfully"}
    raise HTTPException(status_code=404, detail="Post not found")
