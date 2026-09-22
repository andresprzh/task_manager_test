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
