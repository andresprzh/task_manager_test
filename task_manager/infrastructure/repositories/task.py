"""Persistence for the task feature: the lists themselves and the tasks in them.

Both models live here because they are one aggregate — a task only exists
inside a list. A new, unrelated feature gets its own sibling module rather
than more classes in this one.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from task_manager.domain.models import (
    ListTask as DomainListTask,
    Priority,
    Status,
    Task as DomainTask,
)
from task_manager.domain.repositories import ListTaskRepository, TaskRepository
from task_manager.infrastructure.repositories.base import Base, enum_column


class ListTaskORM(Base):
    __tablename__ = "task_lists"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)


class TaskORM(Base):
    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    list_id = Column(
        String(36), ForeignKey("task_lists.id"), nullable=False, index=True
    )
    description = Column(Text, nullable=True)
    status = enum_column(Status, Status.PENDING)
    priority = enum_column(Priority, Priority.MEDIUM)


def _list_to_domain(orm: ListTaskORM) -> DomainListTask:
    """Map a row to the domain model. ``tasks`` is left empty: it is not loaded."""
    return DomainListTask(
        id=UUID(orm.id),
        name=orm.name,
        description=orm.description,
    )


def _task_to_domain(orm: TaskORM) -> DomainTask:
    return DomainTask(
        id=UUID(orm.id),
        title=orm.title,
        list_id=UUID(orm.list_id),
        description=orm.description,
        status=Status(orm.status),
        priority=Priority(orm.priority),
    )


class SQLAlchemyListTaskRepository(ListTaskRepository):
    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory

    async def create(self, task_list: DomainListTask) -> DomainListTask:
        async with self._session_factory() as session:
            orm = ListTaskORM(
                id=str(task_list.id),
                name=task_list.name,
                description=task_list.description,
            )
            session.add(orm)
            await session.commit()
            await session.refresh(orm)
            return _list_to_domain(orm)

    async def delete(self, task_list: DomainListTask) -> UUID:
        async with self._session_factory() as session:
            orm = await session.get(ListTaskORM, str(task_list.id))
            if not orm:
                raise ValueError("List not found")
            await session.delete(orm)
            await session.commit()
            return task_list.id

    async def get(self, id: UUID) -> Optional[DomainListTask]:
        async with self._session_factory() as session:
            orm = await session.get(ListTaskORM, str(id))
            if not orm:
                return None
            return _list_to_domain(orm)

    async def get_with_tasks(self, id: UUID) -> Optional[DomainListTask]:
        async with self._session_factory() as session:
            orm = await session.get(ListTaskORM, str(id))
            if not orm:
                return None
            result = await session.execute(
                select(TaskORM).where(TaskORM.list_id == str(id))
            )
            task_list = _list_to_domain(orm)
            task_list.tasks = [_task_to_domain(row) for row in result.scalars().all()]
            return task_list

    async def list(self) -> List[DomainListTask]:
        async with self._session_factory() as session:
            result = await session.execute(select(ListTaskORM))
            rows = result.scalars().all()
            return [_list_to_domain(row) for row in rows]


class SQLAlchemyTaskRepository(TaskRepository):
    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory

    async def create(self, task: DomainTask) -> DomainTask:
        async with self._session_factory() as session:
            orm = TaskORM(
                id=str(task.id),
                title=task.title,
                list_id=str(task.list_id),
                description=task.description,
                status=task.status,
                priority=task.priority,
            )
            session.add(orm)
            await session.commit()
            await session.refresh(orm)
            return _task_to_domain(orm)

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
            return _task_to_domain(orm)

    async def list(self) -> List[DomainTask]:
        async with self._session_factory() as session:
            result = await session.execute(select(TaskORM))
            rows = result.scalars().all()
            return [_task_to_domain(row) for row in rows]
