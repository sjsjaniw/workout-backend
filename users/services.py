from sqlalchemy import select
from sqlalchemy.orm.strategy_options import joinedload

from database import BaseRepository
from models import Category, SocialAccount, User


class UserRepository(BaseRepository[User]):
    def __init__(self, session):
        super().__init__(User, session)

    async def login_or_register_by_provider_id(
        self, id: int, username: str, provider: str
    ):
        query = (
            select(SocialAccount)
            .where(
                (SocialAccount.provider == provider) & (SocialAccount.social_id == id)
            )
            .options(joinedload(SocialAccount.user))
        )

        account = (await self.session.execute(query)).scalar_one_or_none()

        if account:
            return account.user

        new_user = User(name=username)
        self.session.add(new_user)
        await self.session.flush()

        new_link = SocialAccount(user_id=new_user.id, provider=provider, social_id=id)
        self.session.add(new_link)

        await self.session.commit()
        return new_user

    async def get_by_category_id(self, category_id: int):
        query = select(self.model).join(Category).where(Category.id == category_id)
        return (await self.session.execute(query)).scalar_one_or_none()
