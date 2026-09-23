from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from uuid import UUID


class Priority(str, Enum):
    """Severity layers a task can be classified with, from most to least urgent."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Status(str, Enum):
    """How far along a task is: pending -> in_progress -> completed."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class Task:
    id: UUID
    title: str
    list_id: UUID
    description: Optional[str] = None
    status: Status = Status.PENDING
    priority: Priority = Priority.MEDIUM


@dataclass
class ListTask:
    id: UUID
    name: str
    description: Optional[str] = None
    tasks: List[Task] = field(default_factory=list)
