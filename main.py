from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db import (
    CategoryRepository,
    UserRepository,
    WorkoutRepository,
    get_async_session,
    login_or_register_by_provider_id,
)
from schemas import (
    CategoryCreate,
    CategoryRead,
    UserCreate,
    UserRead,
    WorkoutCreate,
    WorkoutRead,
)

app = FastAPI()

user_router = APIRouter(prefix="/users", tags=["users"])
category_router = APIRouter(prefix="/categories", tags=["categories"])
workoutdata_router = APIRouter(prefix="/workoutsdata", tags=["workoutsdata"])


@user_router.get("/{user_id}")
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

        return await login_or_register_by_provider_id(
            id=user_data.social_id,
            username=user_data.name,
            provider=user_data.provider,
            session=session,
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


@category_router.get("/{category_id}")
async def get_categories_by_user_id(
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
    category_repo = UserRepository(session=session)

    deleted_category = await category_repo.delete_by_id(id=category_id)

    if not deleted_category:
        return HTTPException(status_code=404, detail="Category not found")

    return {f"Category with id {deleted_category.id}": "was deleted"}


@workoutdata_router.get("/{workoutdata_id}")
async def get_workoutdata_by_id(
    workoutdata_id: int, session: AsyncSession = Depends(get_async_session)
):
    workouts_repo = WorkoutRepository(session=session)
    return await workouts_repo.get_by_id(id=workoutdata_id)


@workoutdata_router.post("/", response_model=WorkoutRead)
async def create_workoutdata_handler(
    workout_data: WorkoutCreate, session: AsyncSession = Depends(get_async_session)
):
    workouts_repo = WorkoutRepository(session=session)
    new_workout = await workouts_repo.create(
        user_id=workout_data.user_id,
        category_id=workout_data.category_id,
        quantity=workout_data.quantity,
    )
    return new_workout


@workoutdata_router.delete("/{workoutdata_id}")
async def delete_workoutdata_handler(
    workoutdata_id: int, session: AsyncSession = Depends(get_async_session)
):
    workouts_repo = UserRepository(session=session)

    deleted_workout = await workouts_repo.delete_by_id(id=workoutdata_id)

    if not deleted_workout:
        return HTTPException(status_code=404, detail="Workout not found")

    return {f"Workout with id {deleted_workout.id}": "was deleted"}


app.include_router(user_router)
app.include_router(category_router)
app.include_router(workoutdata_router)
