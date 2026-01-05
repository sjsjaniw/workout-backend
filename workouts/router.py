from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from .schemas import WorkoutCreate, WorkoutRead
from .services import WorkoutRepository

workoutdata_router = APIRouter(prefix="/workoutsdata", tags=["workoutsdata"])


@workoutdata_router.get("/{workoutdata_id}", response_model=WorkoutRead)
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
    workouts_repo = WorkoutRepository(session=session)

    deleted_workout = await workouts_repo.delete_by_id(id=workoutdata_id)

    if not deleted_workout:
        return HTTPException(status_code=404, detail="Workout not found")

    return {f"Workout with id {deleted_workout.id}": "was deleted"}
