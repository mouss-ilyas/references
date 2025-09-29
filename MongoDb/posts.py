from crud.databaseConfig import posts_collection
from typing import List
from bson import ObjectId

from pymongo import MongoClient
import os
url = os.getenv("DATABASE_URL")
client = MongoClient(url, serverSelectionTimeoutMS=10000)
db = client["BlogDB"]
posts_collection = db["posts"]
comments_collection = db["comments"]
users_collection = db["users"]
router = APIRouter()

#post model
class Post(BaseModel):
    title: str
    content: str
    author: str
    
class PostInDB(Post):
    id: str
    author_id:str
#user model
class User(BaseModel):
    username: str
    email: str
    password: str
class UserInDB(User):
    id:str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/", response_model=PostInDB)
async def create_post(post: Post ,user :UserInDB= Depends(login_required)):
    post_dict = post.dict()
    post_dict["author_id"]=user["id"]
    result = posts_collection.insert_one(post_dict)
    post_dict["id"] = str(result.inserted_id)
    post_dict.pop("_id")
    return post_dict

@router.get("/",response_model=List[PostInDB])
async def getAll():
    posts=[]
    for p in posts_collection.find() :
        p["id"]= str(p["_id"])
        p.pop("_id")
        posts.append(p)
    return posts

@router.get("/{id}",response_model=PostInDB)
async def getOne(id:str):
    post = posts_collection.find_one({"_id": ObjectId(id)})
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    post["id"] = str(post["_id"])
    post.pop("_id")
    return post

@router.put("/{post_id}")
async def update_post(post_id: str, post: Post):
    post_dict = post.dict()
    result = posts_collection.update_one({"_id": ObjectId(post_id)}, {"$set": post_dict})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    post_dict["id"] = post_id
    return post_dict

@router.delete("/{id}")
async def deletePost(id: str):
    post = posts_collection.find_one_and_delete({"_id": ObjectId(id)})
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    post["id"] = str(post["_id"])
    post.pop("_id")
    return post
