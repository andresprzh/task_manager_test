from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from task_manager.infrastructure.repositories import (
    init_db_sync,
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
)
from task_manager.infrastructure.api import get_list_router, get_task_router


def create_app() -> FastAPI:
    # initialize async DB and sessionmaker synchronously during app creation
    session_maker = init_db_sync()
    task_repo = SQLAlchemyTaskRepository(session_maker)
    list_repo = SQLAlchemyListTaskRepository(session_maker)

    create_uc = CreateTaskUseCase(task_repo)
    get_uc = GetTaskUseCase(task_repo)
    delete_uc = DeleteTaskUseCase(task_repo)

    create_list_uc = CreateListTaskUseCase(list_repo)
    get_list_uc = GetListTaskUseCase(list_repo)
    list_lists_uc = GetAllListTasksUseCase(list_repo)
    delete_list_uc = DeleteListTaskUseCase(list_repo)

    # Provide OpenAPI metadata and disable default docs URLs so we can customize
    app = FastAPI(
        title="Task Manager (Layered)",
        description="A small demo showing Domain / Application / Infrastructure layers",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json",
    )

    app.include_router(
        get_list_router(create_list_uc, get_list_uc, list_lists_uc, delete_list_uc)
    )
    app.include_router(get_task_router(create_uc, get_uc, delete_uc))

    @app.get("/", include_in_schema=False)
    async def custom_swagger_ui():
        """Serve Swagger UI using FastAPI's built-in helper.

        No extra dependency required — FastAPI includes Swagger UI and ReDoc endpoints.
        """
        return get_swagger_ui_html(
            openapi_url=app.openapi_url, title=f"{app.title} - Swagger UI"
        )

    return app


app = create_app()
