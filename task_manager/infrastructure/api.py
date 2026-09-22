from fastapi import APIRouter, HTTPException
from uuid import UUID
from task_manager.application.schemas import TaskCreate, TaskRead


def get_router(create_uc, get_uc, list_uc, delete_uc) -> APIRouter:
    router = APIRouter(prefix="/tasks", tags=["tasks"])

    @router.post(
        "/",
        response_model=TaskRead,
        status_code=201,
        summary="Create a task",
        response_description="The created task",
    )
    async def create_task(payload: TaskCreate):
        """Create a new task.

        Accepts a `TaskCreate` payload and returns the created `TaskRead`.
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

    @router.get(
        "/",
        response_model=list[TaskRead],
        summary="List tasks",
        response_description="A list of tasks",
    )
    async def list_tasks():
        """Return all tasks."""
        return await list_uc.execute()

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
