from pydantic import BaseModel


class WorkoutCreate(BaseModel):
    user_id: int
    category_id: int
    quantity: int


class WorkoutRead(BaseModel):
    id: int

    class Config:
        from_attributes = True
