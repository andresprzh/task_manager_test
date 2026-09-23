from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from uuid import UUID
from task_manager.domain.models import Priority, Status
from task_manager.application.schemas import (
    ListTaskCreate,
    ListTaskDetailRead,
    ListTaskRead,
    TaskCreate,
    TaskRead,
)


def get_list_router(create_uc, get_uc, list_uc, delete_uc) -> APIRouter:
    router = APIRouter(prefix="/lists", tags=["lists"])

    @router.post(
        "/",
        response_model=ListTaskRead,
        status_code=201,
        summary="Create a task list",
        response_description="The created list",
    )
    async def create_list(payload: ListTaskCreate):
        """Create a new task list.

        Its `id` is what a later `POST /tasks/` passes as `list_id`.
        """
        return await create_uc.execute(payload)

    @router.get(
        "/",
        response_model=list[ListTaskRead],
        summary="List task lists",
        response_description="All task lists",
    )
    async def list_lists():
        """Return every task list. The tasks they own are not included."""
        return await list_uc.execute()

    @router.get(
        "/{list_id}",
        response_model=ListTaskDetailRead,
        summary="Get a task list with its tasks",
        response_description="The list and every task in it",
    )
    async def get_list(
        list_id: UUID,
        status: Optional[Status] = Query(
            None,
            title="Status filter",
            description=(
                "Return only tasks in this state. Omit to return them all. "
                "One of `pending`, `in_progress`, `completed`."
            ),
        ),
        priority: Optional[Priority] = Query(
            None,
            title="Priority filter",
            description=(
                "Return only tasks at this severity layer. Omit to return them "
                "all. One of `high`, `medium`, `low`."
            ),
        ),
    ):
        """Retrieve one task list by UUID, with the tasks that belong to it.

        Unlike `GET /lists/`, this embeds the tasks under `tasks`.

        `status` and `priority` narrow that array, and combine with AND when
        both are given. Neither affects `completed_percentage` — that is always
        measured against every task in the list, so the progress figure stays
        stable no matter how you filter.
        """
        task_list = await get_uc.execute(list_id, status=status, priority=priority)
        if not task_list:
            raise HTTPException(status_code=404, detail="List not found")
        return task_list

    @router.delete(
        "/{list_id}",
        status_code=204,
        summary="Delete a task list",
        response_description="The list was deleted",
    )
    async def delete_list(list_id: UUID):
        """Delete a task list by UUID.

        The tasks pointing at it are left untouched, so they end up orphaned.
        """
        try:
            await delete_uc.execute(list_id)
        except ValueError:
            raise HTTPException(status_code=404, detail="List not found")

    return router


def get_task_router(create_uc, get_uc, delete_uc) -> APIRouter:
    router = APIRouter(prefix="/tasks", tags=["tasks"])

    @router.post(
        "/",
        response_model=TaskRead,
        status_code=201,
        summary="Create a task",
        response_description="The created task",
    )
    async def create_task(payload: TaskCreate):
        """Create a new task inside a list.

        | Field | Required | Notes |
        | --- | --- | --- |
        | `title` | yes | Short name of the task. |
        | `list_id` | yes | UUID of the owning list, from `POST /lists/`. |
        | `description` | no | Free-text detail. Defaults to `null`. |
        | `status` | no | `pending` (default), `in_progress`, `completed`. |
        | `priority` | no | `high`, `medium` (default), `low`. |

        The `id` is generated server-side and returned in the `TaskRead`
        response, so do not send one.
        """
        return await create_uc.execute(payload)

    @router.get(
        "/{task_id}",
        response_model=TaskRead,
        summary="Get a task by ID",
        response_description="The task with the given id",
    )
    async def get_task(task_id: UUID):
        """Retrieve a single task by UUID."""
        task = await get_uc.execute(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    @router.delete(
        "/{task_id}",
        status_code=204,
        summary="Delete a task",
        response_description="The task was deleted",
    )
    async def delete_task(task_id: UUID):
        """Delete a task by UUID."""
        await delete_uc.execute(task_id)

    return router
