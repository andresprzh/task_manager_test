from pydantic import BaseModel, Field, computed_field
from typing import List, Optional
from uuid import UUID

from task_manager.domain.models import Priority, Status


class ListTaskCreate(BaseModel):
    name: str = Field(..., title="Name", example="Groceries")
    description: Optional[str] = Field(
        None, title="Description", example="Everything to buy this week"
    )


class ListTaskRead(BaseModel):
    """A task list on its own. The tasks it owns are not embedded here."""

    id: UUID = Field(..., title="ID", example="9f8d7c6b-5a4e-4d3c-2b1a-0f9e8d7c6b5a")
    name: str = Field(..., example="Groceries")
    description: Optional[str] = Field(None, example="Everything to buy this week")
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "9f8d7c6b-5a4e-4d3c-2b1a-0f9e8d7c6b5a",
                "name": "Groceries",
                "description": "Everything to buy this week",
            }
        },
    }


class TaskCreate(BaseModel):
    """Payload for creating a task.

    Only `title` and `list_id` are required. The server assigns the `id`, so it
    is never accepted here; `status` and `priority` fall back to their defaults
    when omitted.
    """

    title: str = Field(
        ...,
        title="Title",
        description="Short, human-readable name of the task. Required.",
        example="Buy groceries",
    )
    list_id: UUID = Field(
        ...,
        title="List ID",
        description=(
            "UUID of the list that owns this task. Required — a task cannot "
            "exist outside a list. Use the `id` returned by `POST /lists/`."
        ),
        example="9f8d7c6b-5a4e-4d3c-2b1a-0f9e8d7c6b5a",
    )
    description: Optional[str] = Field(
        None,
        title="Description",
        description="Optional free-text detail about the task.",
        example="Milk, eggs, bread",
    )
    status: Status = Field(
        Status.PENDING,
        title="Status",
        description=(
            "How far along the task is. Defaults to `pending`. One of:\n\n"
            "- `pending` — not started yet\n"
            "- `in_progress` — actively being worked on\n"
            "- `completed` — finished; these are what "
            "`completed_percentage` counts on `GET /lists/{list_id}`"
        ),
        example=Status.PENDING,
    )
    priority: Priority = Field(
        Priority.MEDIUM,
        title="Priority",
        description=(
            "Severity layer, from most to least urgent. Defaults to `medium`. "
            "One of:\n\n"
            "- `high` — needs attention soon, ahead of routine work\n"
            "- `medium` — normal, scheduled work\n"
            "- `low` — nice to have, no deadline pressure"
        ),
        example=Priority.MEDIUM,
    )


class TaskRead(BaseModel):
    id: UUID = Field(..., title="ID", example="3fa85f64-5717-4562-b3fc-2c963f66afa6")
    title: str = Field(..., example="Buy groceries")
    list_id: UUID = Field(..., example="9f8d7c6b-5a4e-4d3c-2b1a-0f9e8d7c6b5a")
    description: Optional[str] = Field(None, example="Milk, eggs, bread")
    status: Status = Field(Status.PENDING, example=Status.PENDING)
    priority: Priority = Field(Priority.MEDIUM, example=Priority.MEDIUM)
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "title": "Buy groceries",
                "list_id": "9f8d7c6b-5a4e-4d3c-2b1a-0f9e8d7c6b5a",
                "description": "Milk, eggs, bread",
                "status": "pending",
                "priority": "medium",
            }
        },
    }


class ListTaskDetailRead(ListTaskRead):
    """A task list together with the tasks that belong to it.

    Defined after ``TaskRead`` because it embeds it.
    """

    tasks: List[TaskRead] = Field(
        default_factory=list,
        title="Tasks",
        description=(
            "Tasks in this list, narrowed by the `status` and `priority` query "
            "parameters when they are supplied."
        ),
    )

    # Totals over *every* task in the list, before any filter. Kept out of the
    # response body: they exist only so that filtering `tasks` cannot move
    # `completed_percentage`.
    total_task_count: int = Field(default=0, exclude=True)
    completed_task_count: int = Field(default=0, exclude=True)

    @computed_field(
        title="Completed percentage",
        description=(
            "Share of this list's tasks whose status is `completed`, from 0 to "
            "100. Always measured against every task in the list, so the "
            "`status` and `priority` filters never change it; an empty list is 0."
        ),
        examples=[33.33],
    )
    @property
    def completed_percentage(self) -> float:
        if not self.total_task_count:
            return 0.0
        return round(self.completed_task_count * 100 / self.total_task_count, 2)

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "9f8d7c6b-5a4e-4d3c-2b1a-0f9e8d7c6b5a",
                "name": "Groceries",
                "description": "Everything to buy this week",
                "tasks": [
                    {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "title": "Buy groceries",
                        "list_id": "9f8d7c6b-5a4e-4d3c-2b1a-0f9e8d7c6b5a",
                        "description": "Milk, eggs, bread",
                        "status": "pending",
                        "priority": "medium",
                    }
                ],
                "completed_percentage": 0.0,
            }
        },
    }
