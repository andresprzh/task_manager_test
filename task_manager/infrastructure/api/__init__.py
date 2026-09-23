"""HTTP routers, one module per feature."""

from task_manager.infrastructure.api.task import get_list_router, get_task_router
from task_manager.infrastructure.api.auth import get_auth_router

__all__ = ["get_list_router", "get_task_router", "get_auth_router"]
