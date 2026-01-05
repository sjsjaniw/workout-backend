from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import ASYNC_DATABASE_URL
from models import Base

engine = create_async_engine(url=ASYNC_DATABASE_URL, echo=True, pool_pre_ping=True)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def create(self, auto_commit: bool = True, **kwargs):
        new_model = self.model(**kwargs)
        self.session.add(new_model)
        try:
            if auto_commit:
                await self.session.commit()
                await self.session.refresh(new_model)
            else:
                await self.session.flush()
        except:
            await self.session.rollback()
            raise
        return new_model

    async def get_by_id(self, id: int):
        return (
            await self.session.execute(select(self.model).where(self.model.id == id))
        ).scalar_one_or_none()

    async def delete_by_id(self, id: int, auto_commit: bool = True):
        model = (
            await self.session.execute(select(self.model).where(self.model.id == id))
        ).scalar_one_or_none()

        if not model:
            return None

        await self.session.delete(model)
        try:
            if auto_commit:
                await self.session.commit()
            else:
                await self.session.flush()
        except:
            await self.session.rollback()
            raise

        return model


async def get_async_session():
    async with async_session() as session:
        yield session
