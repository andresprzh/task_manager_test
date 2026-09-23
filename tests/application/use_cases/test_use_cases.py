import uuid

import pytest


from task_manager.domain.models import ListTask, Task, Status, Priority
from task_manager.application.use_cases.task import ListTaskUseCase, TaskUseCase
from task_manager.infrastructure.repositories import (
    SQLAlchemyListTaskRepository,
    SQLAlchemyTaskRepository,
)


@pytest.mark.anyio
async def test_list_use_cases_crud_and_get_with_tasks(session_maker):
    """Test the CRUD operations of list use cases and getting a list with its tasks."""

    task_repo = SQLAlchemyTaskRepository(session_maker)
    list_repo = SQLAlchemyListTaskRepository(session_maker)

    list_uc = ListTaskUseCase(list_repo)
    task_uc = TaskUseCase(task_repo)

    # Create list
    data = type("D", (), {"name": "L1", "description": "d"})()
    created = await list_uc.create(data)
    assert created.name == "L1"

    # Create task in list
    task_data = type(
        "TD",
        (),
        {
            "title": "T1",
            "list_id": created.id,
            "description": "desc",
            "status": Status.PENDING,
            "priority": Priority.MEDIUM,
        },
    )()
    created_task = await task_uc.create(task_data)
    assert created_task.title == "T1"

    # Get list with tasks and filtering
    got = await list_uc.get(created.id)
    assert got is not None
    assert any(t.title == "T1" for t in got.tasks)

    # filtered by status not matching -> empty
    got_empty = await list_uc.get(created.id, status=Status.COMPLETED)
    assert got_empty.tasks == []

    # Update list
    upd = type("U", (), {"name": "L1-v2", "description": None})()
    updated = await list_uc.update(created.id, upd)
    assert updated.name == "L1-v2"

    # Get all lists
    all_lists = await list_uc.get_all()
    assert any(lst.name == "L1-v2" for lst in all_lists)

    # Delete list
    deleted_id = await list_uc.delete(created.id)
    assert deleted_id == created.id


@pytest.mark.anyio
async def test_task_use_cases_update_status_and_delete(session_maker):
    """Test the CRUD operations of task use cases,
    including status update and deletion."""

    task_repo = SQLAlchemyTaskRepository(session_maker)
    list_repo = SQLAlchemyListTaskRepository(session_maker)

    task_uc = TaskUseCase(task_repo)

    # Prepare list and task
    list_id = uuid.uuid4()
    lt = ListTask(id=list_id, name="L", description=None)
    await list_repo.create(lt)

    task_id = uuid.uuid4()
    t = Task(id=task_id, title="T", list_id=list_id, description=None)
    await task_repo.create(t)

    # Update status
    sd = type("SD", (), {"status": Status.COMPLETED})()
    updated = await task_uc.update_status(task_id, sd)
    assert updated.status == Status.COMPLETED

    # Update full task
    ud = type(
        "UD",
        (),
        {
            "title": "T-new",
            "list_id": list_id,
            "description": "now",
            "status": Status.IN_PROGRESS,
            "priority": Priority.HIGH,
        },
    )()
    updated_full = await task_uc.update(task_id, ud)
    assert updated_full.title == "T-new"
    assert updated_full.priority == Priority.HIGH

    # Get task
    got = await task_uc.get(task_id)
    assert got.title == "T-new"

    # Delete task
    deleted = await task_uc.delete(task_id)
    assert deleted == task_id

    # Deleting missing should raise
    with pytest.raises(ValueError):
        await task_uc.delete(task_id)
