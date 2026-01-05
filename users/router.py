from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from .schemas import UserCreate, UserRead
from .services import UserRepository

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/category/", response_model=UserRead)
async def get_user_by_category_id(
    category_id: int, session: AsyncSession = Depends(get_async_session)
):
    user_repo = UserRepository(session=session)

    return await user_repo.get_by_category_id(category_id)


@user_router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    user_repo = UserRepository(session=session)
    return await user_repo.get_by_id(id=user_id)


@user_router.post("/", response_model=UserRead)
async def create_user_handler(
    user_data: UserCreate, session: AsyncSession = Depends(get_async_session)
):
    user_repo = UserRepository(session=session)

    if user_data.social_id:
        if not user_data.provider:
            return HTTPException(
                status_code=400, detail="Provider is required for social register"
            )

        return await user_repo.login_or_register_by_provider_id(
            id=user_data.social_id,
            username=user_data.name,
            provider=user_data.provider,
        )

    new_user = await user_repo.create(name=user_data.name, password=user_data.password)
    return new_user


@user_router.delete("/{user_id}")
async def delete_user_handler(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    user_repo = UserRepository(session=session)

    deleted_user = await user_repo.delete_by_id(id=user_id)

    if not deleted_user:
        return HTTPException(status_code=404, detail="User not found")

    return {f"User with id {deleted_user.id}": "was deleted"}
