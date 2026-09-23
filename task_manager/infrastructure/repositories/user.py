from typing import Optional
from uuid import UUID

from sqlalchemy import Column, String
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from task_manager.domain.models import User as DomainUser
from task_manager.domain.repositories import UserRepository
from task_manager.infrastructure.repositories.base import Base


class UserORM(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)


def _user_to_domain(orm: UserORM) -> DomainUser:
    return DomainUser(
        id=UUID(orm.id),
        username=orm.username,
        email=orm.email,
        hashed_password=orm.hashed_password,
    )


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory

    async def create(self, user: DomainUser) -> DomainUser:
        async with self._session_factory() as session:
            orm = UserORM(
                id=str(user.id),
                username=user.username,
                email=user.email,
                hashed_password=user.hashed_password,
            )
            session.add(orm)
            await session.commit()
            await session.refresh(orm)
            return _user_to_domain(orm)

    async def get(self, id: UUID) -> Optional[DomainUser]:
        async with self._session_factory() as session:
            result = await session.execute(select(UserORM).where(UserORM.id == str(id)))
            orm = result.scalar_one_or_none()
            return _user_to_domain(orm) if orm else None

    async def get_by_username(self, username: str) -> Optional[DomainUser]:
        async with self._session_factory() as session:
            result = await session.execute(
                select(UserORM).where(UserORM.username == username)
            )
            orm = result.scalar_one_or_none()
            return _user_to_domain(orm) if orm else None
