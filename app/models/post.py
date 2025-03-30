from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
