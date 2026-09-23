from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from task_manager.domain.models import ListTask, Task


class TaskRepository(ABC):
    @abstractmethod
    async def create(self, task: Task) -> Task:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: UUID) -> Optional[Task]:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[Task]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, task: Task) -> Task:
        """Persist an already-loaded task. Which fields a caller is allowed to
        change is an application concern, not a persistence one."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, task: Task) -> UUID:
        raise NotImplementedError


class ListTaskRepository(ABC):
    @abstractmethod
    async def create(self, task_list: ListTask) -> ListTask:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: UUID) -> Optional[ListTask]:
        """Fetch the list on its own. ``tasks`` is left empty."""
        raise NotImplementedError

    @abstractmethod
    async def get_with_tasks(self, id: UUID) -> Optional[ListTask]:
        """Fetch the whole aggregate: the list with ``tasks`` populated."""
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[ListTask]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, task_list: ListTask) -> ListTask:
        """Persist an already-loaded list. Only its own fields are written;
        the tasks it owns are managed through ``TaskRepository``."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, task_list: ListTask) -> UUID:
        raise NotImplementedError
