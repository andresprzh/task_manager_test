from fastapi import APIRouter, HTTPException
from task_manager.application.schemas.user import (
    UserCreate,
    UserRead,
    LoginRequest,
    Token,
)
from task_manager.application.use_cases.auth import AuthUseCase


def get_auth_router(auth_uc: AuthUseCase) -> APIRouter:
    router = APIRouter(prefix="/auth", tags=["auth"])

    @router.post(
        "/register",
        response_model=UserRead,
        status_code=201,
        summary="Register a new user",
        response_description="The created user",
    )
    async def register(payload: UserCreate):
        """Register a new user account.

        | Field | Required | Notes |
        | --- | --- | --- |
        | `username` | yes | Unique username for login. |
        | `email` | yes | User's email address. |
        | `password` | yes | Password (min 6 characters). |
        """
        try:
            return await auth_uc.register(payload)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.post(
        "/login",
        response_model=Token,
        summary="Login and get JWT token",
        response_description="JWT access token",
    )
    async def login(payload: LoginRequest):
        """Login with username and password to receive a JWT token.

        | Field | Required | Notes |
        | --- | --- | --- |
        | `username` | yes | Username of the account. |
        | `password` | yes | Password of the account. |

        The returned `access_token` is a JWT that must be included in the
        `Authorization` header as `Bearer <token>` for protected endpoints.
        """
        try:
            return await auth_uc.login(payload)
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid username or password")

    return router
