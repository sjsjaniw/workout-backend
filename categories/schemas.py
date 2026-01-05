from pydantic import BaseModel


class CategoryCreate(BaseModel):
    user_id: int
    name: str


class CategoryRead(BaseModel):
    id: int
    name: str
    user_id: int

    class Config:
        from_attributes = True
