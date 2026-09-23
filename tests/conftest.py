import pytest


@pytest.fixture
def anyio_backend():
    """Run ``@pytest.mark.anyio`` tests on asyncio only.

    The repository, use cases and API layers are async. The pytest plugin that
    runs them ships with ``anyio`` (already a FastAPI dependency), so no extra
    package is needed: mark a coroutine test with ``@pytest.mark.anyio`` and it
    will be awaited using this backend.
    """
    return "asyncio"


@pytest.fixture
async def session_maker(tmp_path):
    """Provide an async SQLAlchemy sessionmaker backed by a temporary SQLite file.

    This fixture creates a per-test SQLite file and initializes the schema so
    tests can use the real repositories against a lightweight file DB.
    """
    from task_manager.infrastructure.repositories import init_async_db

    db_file = tmp_path / "test_db.sqlite"
    db_url = f"sqlite+aiosqlite:///{db_file}"
    maker = await init_async_db(db_url)
    return maker


@pytest.fixture
def fake_list_usecases():
    """Provide a lightweight in-memory fake for list use-cases for API tests."""

    class FakeListUseCases:
        def __init__(self):
            self.storage = {}

        async def create(self, data):
            from uuid import uuid4

            from task_manager.domain.models import ListTask

            lt = ListTask(id=uuid4(), name=data.name, description=data.description)
            self.storage[str(lt.id)] = lt
            return lt

        async def get_all(self):
            return list(self.storage.values())

        async def get(self, id, status=None, priority=None):
            return self.storage.get(str(id))

        async def update(self, id, data):
            lt = self.storage.get(str(id))
            if not lt:
                return None
            lt.name = data.name
            lt.description = data.description
            self.storage[str(id)] = lt
            return lt

        async def delete(self, id):
            lt = self.storage.get(str(id))
            if not lt:
                raise ValueError("List not found")
            del self.storage[str(id)]

    return FakeListUseCases()


@pytest.fixture
def fake_task_usecases():
    """Provide a lightweight in-memory fake for task use-cases for API tests."""

    class FakeTaskUseCases:
        def __init__(self):
            self.storage = {}

        async def create(self, data):
            from uuid import uuid4

            from task_manager.domain.models import Task

            t = Task(
                id=uuid4(),
                title=data.title,
                list_id=data.list_id,
                description=data.description,
                status=data.status,
                priority=data.priority,
                user_id=getattr(data, "user_id", None),
            )
            self.storage[str(t.id)] = t
            return t

        async def get(self, id):
            return self.storage.get(str(id))

        async def update(self, id, data):
            t = self.storage.get(str(id))
            if not t:
                return None
            t.title = data.title
            t.list_id = data.list_id
            t.description = data.description
            t.status = data.status
            t.priority = data.priority
            t.user_id = getattr(data, "user_id", None)
            self.storage[str(id)] = t
            return t

        async def update_status(self, id, data):
            t = self.storage.get(str(id))
            if not t:
                return None
            t.status = data.status
            self.storage[str(id)] = t
            return t

        async def delete(self, id):
            if str(id) not in self.storage:
                raise ValueError("Task not found")
            del self.storage[str(id)]

    return FakeTaskUseCases()
