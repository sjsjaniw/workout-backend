from pydantic import BaseModel


class UserCreate(BaseModel):
    social_id: int | None
    provider: str | None
    name: str
    password: str | None


class CategoryCreate(BaseModel):
    user_id: int
    name: str


class WorkoutCreate(BaseModel):
    user_id: int
    category_id: int
    quantity: int


class UserRead(BaseModel):
    id: int
    name: str | None

    class Config:
        from_attributes = True


class CategoryRead(BaseModel):
    id: int

    class Config:
        from_attributes = True


class WorkoutRead(BaseModel):
    id: int

    class Config:
        from_attributes = True
