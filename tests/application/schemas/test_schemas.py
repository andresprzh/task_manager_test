import uuid

import pytest
from pydantic import ValidationError

from task_manager.application.schemas.task import (
    ListTaskCreate,
    ListTaskUpdate,
    TaskCreate,
    TaskUpdate,
    TaskStatusUpdate,
    TaskRead,
    ListTaskDetailRead,
)
from task_manager.domain.models import (
    Task as DomainTask,
    ListTask as DomainListTask,
    Status,
    Priority,
)


def test_list_task_create_and_update_extra_forbidden():
    """Test that ListTaskCreate and ListTaskUpdate schemas forbid extra fields
    and validate correctly."""

    # valid create
    payload = {"name": "Groceries", "description": "x"}
    obj = ListTaskCreate.model_validate(payload)
    assert obj.name == "Groceries"

    # update forbids extra fields
    with pytest.raises(ValidationError):
        ListTaskUpdate.model_validate({"name": "A", "extra": "no"})


def test_task_create_and_update_extra_forbidden():
    """Test that TaskCreate, TaskUpdate, and TaskStatusUpdate schemas forbid
    extra fields."""

    # valid create
    payload = {
        "title": "Buy milk",
        "list_id": str(uuid.uuid4()),
        "description": "2 liters",
        "status": Status.PENDING,
        "priority": Priority.MEDIUM,
    }
    obj = TaskCreate.model_validate(payload)
    assert obj.title == "Buy milk"

    # update forbids extra fields
    with pytest.raises(ValidationError):
        TaskUpdate.model_validate({**payload, "extra": 123})

    # status update forbids extra fields
    with pytest.raises(ValidationError):
        TaskStatusUpdate.model_validate({"status": Status.COMPLETED, "extra": 1})


def test_task_update_and_status_update_forbid_extra():
    """Test that TaskUpdate and TaskStatusUpdate schemas forbid extra fields."""

    # TaskUpdate should forbid unknown keys
    base = {
        "title": "T",
        "list_id": str(uuid.uuid4()),
        "description": None,
    }
    with pytest.raises(ValidationError):
        TaskUpdate.model_validate({**base, "id": "not-allowed"})

    # TaskStatusUpdate forbids extras and requires status
    with pytest.raises(ValidationError):
        TaskStatusUpdate.model_validate({"status": "completed", "extra": 1})


def test_taskread_from_attributes_and_list_detail_completed_percentage():
    """
    Test that TaskRead can be validated from a domain object and that
    ListTaskDetailRead computes completed_percentage correctly.
    """

    list_id = uuid.uuid4()
    task_id = uuid.uuid4()

    domain_task = DomainTask(
        id=task_id,
        title="Buy",
        list_id=list_id,
        description="d",
        status=Status.PENDING,
        priority=Priority.MEDIUM,
    )

    # TaskRead can be validated from a domain object (from_attributes=True)
    tr = TaskRead.model_validate(domain_task)
    assert tr.id == task_id
    assert tr.title == "Buy"

    # List detail with tasks: compute completed_percentage
    domain_list = DomainListTask(id=list_id, name="L", description=None)
    domain_list.tasks = [domain_task]
    # set totals as attributes so computed_field uses them
    domain_list.total_task_count = 3
    domain_list.completed_task_count = 1

    ldr = ListTaskDetailRead.model_validate(domain_list)
    # completed_percentage = round(1 * 100 / 3, 2) -> 33.33
    assert ldr.completed_percentage == 33.33
