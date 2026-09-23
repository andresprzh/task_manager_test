from typing import List, Optional
from uuid import uuid4, UUID
from task_manager.domain.models import ListTask, Priority, Status, Task
from task_manager.domain.repositories import ListTaskRepository, TaskRepository
from task_manager.application.schemas import (
    ListTaskCreate,
    ListTaskDetailRead,
    ListTaskRead,
    ListTaskUpdate,
    TaskCreate,
    TaskRead,
    TaskStatusUpdate,
    TaskUpdate,
)


class CreateListTaskUseCase:
    def __init__(self, repo: ListTaskRepository):
        self.repo = repo

    async def execute(self, data: ListTaskCreate) -> ListTaskRead:
        task_list = ListTask(
            id=uuid4(),
            name=data.name,
            description=data.description,
        )
        created = await self.repo.create(task_list)
        return ListTaskRead.model_validate(created)


class DeleteListTaskUseCase:
    def __init__(self, repo: ListTaskRepository):
        self.repo = repo

    async def execute(self, id: UUID) -> UUID:
        task_list = await self.repo.get(id)
        if not task_list:
            raise ValueError("List not found")

        return await self.repo.delete(task_list)


class UpdateListTaskUseCase:
    """Replace a list's own fields, leaving the tasks inside it alone."""

    def __init__(self, repo: ListTaskRepository):
        self.repo = repo

    async def execute(self, id: UUID, data: ListTaskUpdate) -> Optional[ListTaskRead]:
        task_list = await self.repo.get(id)
        if not task_list:
            return None

        task_list.name = data.name
        task_list.description = data.description
        updated = await self.repo.update(task_list)
        return ListTaskRead.model_validate(updated)


class GetListTaskUseCase:
    """Read one list together with the tasks it owns.

    ``status`` and ``priority`` narrow the tasks that come back. They are
    applied here rather than in SQL because the whole list has to be loaded
    anyway to work out ``completed_percentage``, which is deliberately measured
    against every task and so ignores both filters.
    """

    def __init__(self, repo: ListTaskRepository):
        self.repo = repo

    async def execute(
        self,
        id: UUID,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
    ) -> Optional[ListTaskDetailRead]:
        task_list = await self.repo.get_with_tasks(id)
        if not task_list:
            return None

        every_task = task_list.tasks
        matching = [
            task
            for task in every_task
            if (status is None or task.status is status)
            and (priority is None or task.priority is priority)
        ]

        return ListTaskDetailRead(
            id=task_list.id,
            name=task_list.name,
            description=task_list.description,
            tasks=[TaskRead.model_validate(task) for task in matching],
            total_task_count=len(every_task),
            completed_task_count=sum(
                1 for task in every_task if task.status is Status.COMPLETED
            ),
        )


class GetAllListTasksUseCase:
    def __init__(self, repo: ListTaskRepository):
        self.repo = repo

    async def execute(self) -> List[ListTaskRead]:
        task_lists = await self.repo.list()
        return [ListTaskRead.model_validate(tl) for tl in task_lists]


class CreateTaskUseCase:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def execute(self, data: TaskCreate) -> TaskRead:
        task = Task(
            id=uuid4(),
            title=data.title,
            list_id=data.list_id,
            description=data.description,
            status=data.status,
            priority=data.priority,
        )
        created = await self.repo.create(task)
        return TaskRead.model_validate(created)


class DeleteTaskUseCase:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def execute(self, id: UUID) -> bool:
        task = await self.repo.get(id)
        if not task:
            raise ValueError("Task not found")

        deleted = await self.repo.delete(task)

        return deleted


class UpdateTaskUseCase:
    """Replace every mutable field of a task, keeping only its id."""

    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def execute(self, id: UUID, data: TaskUpdate) -> Optional[TaskRead]:
        task = await self.repo.get(id)
        if not task:
            return None

        task.title = data.title
        task.list_id = data.list_id
        task.description = data.description
        task.status = data.status
        task.priority = data.priority
        updated = await self.repo.update(task)
        return TaskRead.model_validate(updated)


class UpdateTaskStatusUseCase:
    """Move a task to a new status, leaving every other field untouched."""

    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def execute(self, id: UUID, data: TaskStatusUpdate) -> Optional[TaskRead]:
        task = await self.repo.get(id)
        if not task:
            return None

        task.status = data.status
        updated = await self.repo.update(task)
        return TaskRead.model_validate(updated)


class GetTaskUseCase:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def execute(self, id: UUID) -> Optional[TaskRead]:
        task = await self.repo.get(id)
        if not task:
            return None
        return TaskRead.model_validate(task)
