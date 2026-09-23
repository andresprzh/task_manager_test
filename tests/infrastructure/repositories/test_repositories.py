import uuid

import pytest

from task_manager.domain.models import ListTask, Task, Priority, Status
from task_manager.infrastructure.repositories import (
    SQLAlchemyListTaskRepository,
    SQLAlchemyTaskRepository,
)


@pytest.mark.anyio
async def test_list_repository_crud(session_maker):
    """Test CRUD operations of SQLAlchemyListTaskRepository with SQLite."""
    list_repo = SQLAlchemyListTaskRepository(session_maker)

    # create
    list_id = uuid.uuid4()
    domain_list = ListTask(id=list_id, name="My List", description="desc")
    created = await list_repo.create(domain_list)
    assert created.id == list_id
    assert created.name == "My List"

    # get
    fetched = await list_repo.get(list_id)
    assert fetched is not None
    assert fetched.id == list_id

    # list
    all_lists = await list_repo.list()
    assert any(lst.id == list_id for lst in all_lists)

    # update
    domain_list.name = "Renamed"
    domain_list.description = None
    updated = await list_repo.update(domain_list)
    assert updated.name == "Renamed"
    assert updated.description is None

    # delete
    deleted_id = await list_repo.delete(domain_list)
    assert deleted_id == list_id
    assert await list_repo.get(list_id) is None


@pytest.mark.anyio
async def test_task_repository_and_get_with_tasks(session_maker):
    """Test CRUD operations and get_with_tasks for task/list repositories."""
    list_repo = SQLAlchemyListTaskRepository(session_maker)
    task_repo = SQLAlchemyTaskRepository(session_maker)

    # create a list
    list_id = uuid.uuid4()
    domain_list = ListTask(id=list_id, name="TL", description=None)
    await list_repo.create(domain_list)

    # create a task
    task_id = uuid.uuid4()
    user_id = uuid.uuid4()
    domain_task = Task(
        id=task_id,
        title="T1",
        list_id=list_id,
        description="task desc",
        status=Status.PENDING,
        priority=Priority.MEDIUM,
        user_id=user_id,
    )
    created_task = await task_repo.create(domain_task)
    assert created_task.id == task_id
    assert created_task.title == "T1"
    assert created_task.user_id == user_id

    # get
    fetched = await task_repo.get(task_id)
    assert fetched is not None
    assert fetched.id == task_id

    # list tasks
    tasks = await task_repo.list()
    assert any(t.id == task_id for t in tasks)

    # get_with_tasks on the list
    list_with_tasks = await list_repo.get_with_tasks(list_id)
    assert list_with_tasks is not None
    assert any(t.id == task_id for t in list_with_tasks.tasks)

    # update task
    new_user_id = uuid.uuid4()
    domain_task.title = "T1 updated"
    domain_task.status = Status.IN_PROGRESS
    domain_task.user_id = new_user_id
    updated = await task_repo.update(domain_task)
    assert updated.title == "T1 updated"
    assert updated.status == Status.IN_PROGRESS
    assert updated.user_id == new_user_id

    # delete task
    deleted = await task_repo.delete(domain_task)
    assert deleted == task_id
    assert await task_repo.get(task_id) is None
