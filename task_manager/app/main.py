from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from task_manager.infrastructure.repository_sqlalchemy import (
    init_db_sync,
    SQLAlchemyTaskRepository,
)
from task_manager.application.use_cases import (
    CreateTaskUseCase,
    DeleteTaskUseCase,
    GetTaskUseCase,
    ListTasksUseCase,
)
from task_manager.infrastructure.api import get_router


def create_app() -> FastAPI:
    # initialize async DB and sessionmaker synchronously during app creation
    session_maker = init_db_sync()
    repo = SQLAlchemyTaskRepository(session_maker)

    create_uc = CreateTaskUseCase(repo)
    get_uc = GetTaskUseCase(repo)
    list_uc = ListTasksUseCase(repo)
    delete_uc = DeleteTaskUseCase(repo)

    # Provide OpenAPI metadata and disable default docs URLs so we can customize
    app = FastAPI(
        title="Task Manager (Layered)",
        description="A small demo showing Domain / Application / Infrastructure layers",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json",
    )

    app.include_router(get_router(create_uc, get_uc, list_uc, delete_uc))

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
