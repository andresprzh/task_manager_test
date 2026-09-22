from typing import Optional, List
from uuid import UUID
import asyncio

from sqlalchemy import Column, String, Text, Boolean
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.future import select

from task_manager.domain.models import Task as DomainTask
from task_manager.domain.repository import TaskRepository

Base = declarative_base()


class TaskORM(Base):
    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False, nullable=False)


class SQLAlchemyTaskRepository(TaskRepository):
    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory

    async def create(self, task: DomainTask) -> DomainTask:
        async with self._session_factory() as session:  # type: AsyncSession
            orm = TaskORM(
                id=str(task.id),
                title=task.title,
                description=task.description,
                completed=task.completed,
            )
            session.add(orm)
            await session.commit()
            await session.refresh(orm)
            return DomainTask(
                id=UUID(orm.id),
                title=orm.title,
                description=orm.description,
                completed=orm.completed,
            )

    async def delete(self, task: DomainTask) -> UUID:
        async with self._session_factory() as session:
            orm = await session.get(TaskORM, str(task.id))
            if not orm:
                raise ValueError("Task not found")
            await session.delete(orm)
            await session.commit()
            return task.id

    async def get(self, id: UUID) -> Optional[DomainTask]:
        async with self._session_factory() as session:
            orm = await session.get(TaskORM, str(id))
            if not orm:
                return None
            return DomainTask(
                id=UUID(orm.id),
                title=orm.title,
                description=orm.description,
                completed=orm.completed,
            )

    async def list(self) -> List[DomainTask]:
        async with self._session_factory() as session:
            result = await session.execute(select(TaskORM))
            rows = result.scalars().all()
            return [
                DomainTask(
                    id=UUID(r.id),
                    title=r.title,
                    description=r.description,
                    completed=r.completed,
                )
                for r in rows
            ]


async def init_async_db(
    db_url: str = "sqlite+aiosqlite:///./task_manager.db",
) -> sessionmaker:
    """Initialize the database and return an async sessionmaker."""
    engine = create_async_engine(db_url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    return maker


def init_db_sync(db_url: str = "sqlite+aiosqlite:///./task_manager.db") -> sessionmaker:
    # helper for synchronous startup code
    return asyncio.run(init_async_db(db_url))
