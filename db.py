from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm.strategy_options import joinedload

from config import ASYNC_DATABASE_URL
from models import Base, Category, SocialAccount, User, WorkoutData

engine = create_async_engine(url=ASYNC_DATABASE_URL, echo=True)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session():
    async with async_session() as session:
        yield session


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


class UserRepository(BaseRepository[User]):
    def __init__(self, session):
        super().__init__(User, session)


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, session):
        super().__init__(Category, session)


class WorkoutRepository(BaseRepository[WorkoutData]):
    def __init__(self, session):
        super().__init__(WorkoutData, session)


async def login_or_register_by_provider_id(
    id: int, username: str, provider: str, session: AsyncSession
):
    query = (
        select(SocialAccount)
        .where((SocialAccount.provider == provider) & (SocialAccount.social_id == id))
        .options(joinedload(SocialAccount.user))
    )

    account = (await session.execute(query)).scalar_one_or_none()

    if account:
        return account.user

    new_user = User(name=username)
    session.add(new_user)
    await session.flush()

    new_link = SocialAccount(user_id=new_user.id, provider=provider, social_id=id)
    session.add(new_link)

    await session.commit()
    return new_user
