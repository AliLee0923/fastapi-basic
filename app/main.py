from fastapi import FastAPI
from routes import auth, post

app = FastAPI()
app.include_router(auth.router)
app.include_router(post.router)