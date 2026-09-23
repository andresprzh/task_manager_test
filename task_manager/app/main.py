from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from task_manager.infrastructure.repositories import (
    init_async_db,
    SQLAlchemyListTaskRepository,
    SQLAlchemyTaskRepository,
)
from task_manager.application.use_cases import ListTaskUseCase, TaskUseCase
from task_manager.infrastructure.api import get_list_router, get_task_router


# Provide OpenAPI metadata and disable default docs URLs so we can customize
app = FastAPI(
    title="Task Manager (Layered)",
    description="A small demo showing Domain / Application / Infrastructure layers",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url="/openapi.json",
)


@app.on_event("startup")
async def startup():
    """Initialize the async DB and register routers when the app starts.

    Doing DB initialization here avoids calling `asyncio.run` from code that
    may already be running inside an event loop (this happens with
    `uvicorn --reload`).
    """
    session_maker = await init_async_db()

    task_repo = SQLAlchemyTaskRepository(session_maker)
    list_repo = SQLAlchemyListTaskRepository(session_maker)

    task_uc = TaskUseCase(task_repo)
    list_uc = ListTaskUseCase(list_repo)

    app.include_router(get_list_router(list_uc))
    app.include_router(get_task_router(task_uc))


@app.get("/", include_in_schema=False)
async def custom_swagger_ui():
    """Serve Swagger UI using FastAPI's built-in helper.

    No extra dependency required — FastAPI includes Swagger UI and ReDoc endpoints.
    """
    return get_swagger_ui_html(
        openapi_url=app.openapi_url, title=f"{app.title} - Swagger UI"
    )
