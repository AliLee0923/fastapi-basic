from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from schemas.post import PostCreate, PostOut
from services import post as post_service, auth as auth_service
from db import get_db
from typing import List

router = APIRouter()

@router.post("/add_post")
def add_post(
    post: PostCreate,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = auth_service.get_current_user(token, db)
    return post_service.add_post(user.id, post, db)

@router.get("/get_posts", response_model=List[PostOut])
def get_posts(
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = auth_service.get_current_user(token, db)
    return post_service.get_posts(user.id, db)

@router.delete("/delete_post/{post_id}")
def delete_post(
    post_id: int,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = auth_service.get_current_user(token, db)
    post_service.delete_post(post_id, user.id, db)
    return {"detail": "Post deleted"}