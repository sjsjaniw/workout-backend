from pydantic import BaseModel


class UserCreate(BaseModel):
    social_id: int | None
    provider: str | None
    name: str
    password: str | None


class UserRead(BaseModel):
    id: int
    name: str | None

    class Config:
        from_attributes = True
