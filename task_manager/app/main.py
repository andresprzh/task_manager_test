from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from task_manager.infrastructure.repositories import (
    init_async_db,
    SQLAlchemyListTaskRepository,
    SQLAlchemyTaskRepository,
)
from task_manager.application.use_cases import (
    CreateListTaskUseCase,
    CreateTaskUseCase,
    DeleteListTaskUseCase,
    DeleteTaskUseCase,
    GetAllListTasksUseCase,
    GetListTaskUseCase,
    GetTaskUseCase,
    UpdateListTaskUseCase,
    UpdateTaskStatusUseCase,
    UpdateTaskUseCase,
)
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

    create_uc = CreateTaskUseCase(task_repo)
    get_uc = GetTaskUseCase(task_repo)
    update_uc = UpdateTaskUseCase(task_repo)
    update_status_uc = UpdateTaskStatusUseCase(task_repo)
    delete_uc = DeleteTaskUseCase(task_repo)

    create_list_uc = CreateListTaskUseCase(list_repo)
    get_list_uc = GetListTaskUseCase(list_repo)
    list_lists_uc = GetAllListTasksUseCase(list_repo)
    update_list_uc = UpdateListTaskUseCase(list_repo)
    delete_list_uc = DeleteListTaskUseCase(list_repo)

    app.include_router(
        get_list_router(
            create_list_uc,
            get_list_uc,
            list_lists_uc,
            update_list_uc,
            delete_list_uc,
        )
    )
    app.include_router(
        get_task_router(create_uc, get_uc, update_uc, update_status_uc, delete_uc)
    )


@app.get("/", include_in_schema=False)
async def custom_swagger_ui():
    """Serve Swagger UI using FastAPI's built-in helper.

    No extra dependency required — FastAPI includes Swagger UI and ReDoc endpoints.
    """
    return get_swagger_ui_html(
        openapi_url=app.openapi_url, title=f"{app.title} - Swagger UI"
    )
