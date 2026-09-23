from uuid import uuid4

from task_manager.domain.models import ListTask, Priority, Status, Task


def test_task_model_defaults():
    """Test that the Task model initializes with default values for optional fields."""

    task_id = uuid4()
    list_id = uuid4()
    task = Task(id=task_id, title="Write release notes", list_id=list_id)

    assert task.id == task_id
    assert task.title == "Write release notes"
    assert task.list_id == list_id
    assert task.description is None
    assert task.status is Status.PENDING
    assert task.priority is Priority.MEDIUM


def test_list_task_holds_many_tasks():
    """Test that the ListTask model can hold multiple Task instances."""

    list_id = uuid4()
    first = Task(id=uuid4(), title="Draft changelog", list_id=list_id)
    second = Task(
        id=uuid4(),
        title="Ship hotfix",
        list_id=list_id,
        status=Status.IN_PROGRESS,
        priority=Priority.HIGH,
    )
    task_list = ListTask(id=list_id, name="Release", tasks=[first, second])

    assert task_list.tasks == [first, second]
    assert all(task.list_id == task_list.id for task in task_list.tasks)


def test_list_task_defaults_to_no_tasks():
    """Test that a new ListTask initializes with an empty list of tasks by default."""

    task_list = ListTask(id=uuid4(), name="Inbox")

    assert task_list.tasks == []
