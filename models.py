from datetime import datetime, timezone

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, primary_key=True, autoincrement=True
    )


class User(Base):
    __tablename__ = "users"
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    password: Mapped[str | None] = mapped_column(String(255), nullable=True)

    categories: Mapped[list["Category"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    workouts: Mapped[list["WorkoutData"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    social_accounts: Mapped[list["SocialAccount"]] = relationship(back_populates="user")


class Category(Base):
    __tablename__ = "categories"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)

    user: Mapped["User"] = relationship(back_populates="categories")
    workouts: Mapped[list["WorkoutData"]] = relationship(
        back_populates="category", cascade="all, delete-orphan"
    )


class WorkoutData(Base):
    __tablename__ = "workoutdata"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="workouts")
    category: Mapped["Category"] = relationship(back_populates="workouts")

    quantity: Mapped[int] = mapped_column(nullable=False)
    time: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )


class SocialAccount(Base):
    __tablename__ = "social_accounts"

    user: Mapped["User"] = relationship(back_populates="social_accounts")
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    social_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint("provider", "social_id", name="uq_provider_social_id"),
    )
