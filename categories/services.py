from sqlalchemy import select

from database import BaseRepository
from models import Category


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, session):
        super().__init__(Category, session)

    async def get_all_by_user_id(self, id: int):
        query = select(self.model).where(self.model.user_id == id)
        categories = await self.session.execute(query)

        return categories.scalars().all()
