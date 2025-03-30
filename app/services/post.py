from sqlalchemy.orm import Session
from models.post import Post
from schemas.post import PostCreate
from fastapi import HTTPException
from cachetools import TTLCache

cache = TTLCache(maxsize=100, ttl=300)

def add_post(user_id: int, post: PostCreate, db: Session):
    new_post = Post(text=post.text, owner_id=user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_posts(user_id: int, db: Session):
    if user_id in cache:
        return cache[user_id]
    posts = db.query(Post).filter(Post.owner_id == user_id).all()
    cache[user_id] = posts
    return posts

def delete_post(post_id: int, user_id: int, db: Session):
    post = db.query(Post).filter(Post.id == post_id, Post.owner_id == user_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    cache.pop(user_id, None)
