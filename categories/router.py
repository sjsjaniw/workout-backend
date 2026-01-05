from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from .schemas import CategoryCreate, CategoryRead
from .services import CategoryRepository

category_router = APIRouter(prefix="/categories", tags=["categories"])


@category_router.get("/user", response_model=list[CategoryRead])
async def get_all_categories_by_user_id(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    category_repo = CategoryRepository(session=session)
    return await category_repo.get_all_by_user_id(id=user_id)


@category_router.get("/{category_id}", response_model=CategoryRead)
async def get_categories_by_id(
    category_id: int, session: AsyncSession = Depends(get_async_session)
):
    category_repo = CategoryRepository(session=session)
    return await category_repo.get_by_id(id=category_id)


@category_router.post("/", response_model=CategoryRead)
async def create_category_handler(
    category_data: CategoryCreate, session: AsyncSession = Depends(get_async_session)
):
    category_repo = CategoryRepository(session=session)
    new_category = await category_repo.create(
        user_id=category_data.user_id, name=category_data.name
    )
    return new_category


@category_router.delete("/{category_id}")
async def delete_category_handler(
    category_id: int, session: AsyncSession = Depends(get_async_session)
):
    category_repo = CategoryRepository(session=session)

    deleted_category = await category_repo.delete_by_id(id=category_id)

    if not deleted_category:
        return HTTPException(status_code=404, detail="Category not found")

    return {f"Category with id {deleted_category.id}": "was deleted"}
