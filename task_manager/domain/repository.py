from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from task_manager.domain.models import Task


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
    async def delete(self, task: Task) -> UUID:
        raise NotImplementedError
