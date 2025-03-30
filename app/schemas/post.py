from pydantic import BaseModel, constr

class PostCreate(BaseModel):
    text: constr(max_length=1_000_000)

class PostOut(BaseModel):
    id: int
    text: str