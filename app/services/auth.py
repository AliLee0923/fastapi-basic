import hashlib
import uuid
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.user import User
from schemas.user import UserCreate

fake_token_store = {}

def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(user: UserCreate, db: Session):
    db_user = User(email=user.email, hashed_password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user or user.hashed_password != hash_password(password):
        return None
    token = str(uuid.uuid4())
    fake_token_store[token] = user.id
    return token

def get_current_user(token: str, db: Session):
    user_id = fake_token_store.get(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return db.query(User).get(user_id)