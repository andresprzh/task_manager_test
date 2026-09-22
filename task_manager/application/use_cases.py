from typing import List, Optional
from uuid import uuid4, UUID
from task_manager.domain.models import Task
from task_manager.domain.repository import TaskRepository
from task_manager.application.schemas import TaskCreate, TaskRead


class CreateTaskUseCase:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def execute(self, data: TaskCreate) -> TaskRead:
        task = Task(id=uuid4(), title=data.title, description=data.description)
        created = await self.repo.create(task)
        return TaskRead.from_orm(created)


class DeleteTaskUseCase:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def execute(self, id: UUID) -> None:
        task = await self.repo.get(id)
        if not task:
            raise ValueError("Task not found")

        deleted = await self.repo.delete(task)

        return deleted


class GetTaskUseCase:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def execute(self, id: UUID) -> Optional[TaskRead]:
        task = await self.repo.get(id)
        if not task:
            return None
        return TaskRead.from_orm(task)


class ListTasksUseCase:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def execute(self) -> List[TaskRead]:
        tasks = await self.repo.list()
        return [TaskRead.from_orm(t) for t in tasks]
