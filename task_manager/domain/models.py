from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class Task:
    id: UUID
    title: str
    description: Optional[str] = None
    completed: bool = False
