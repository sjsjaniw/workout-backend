from database import BaseRepository
from models import WorkoutData


class WorkoutRepository(BaseRepository[WorkoutData]):
    def __init__(self, session):
        super().__init__(WorkoutData, session)
