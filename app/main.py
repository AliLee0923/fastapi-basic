from fastapi import FastAPI
from routes import auth, post
from db import Base, engine

app = FastAPI()
app.include_router(auth.router)
app.include_router(post.router)

Base.metadata.create_all(bind=engine)