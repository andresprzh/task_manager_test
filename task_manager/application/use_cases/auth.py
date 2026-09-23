from uuid import uuid4
from task_manager.domain.models import User
from task_manager.domain.repositories import UserRepository
from task_manager.application.schemas.user import (
    UserCreate,
    UserRead,
    LoginRequest,
    Token,
)
from task_manager.application.security.password import hash_password, verify_password
from task_manager.application.security.jwt import create_access_token


class AuthUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register(self, data: UserCreate) -> UserRead:
        existing_user = await self.repo.get_by_username(data.username)
        if existing_user:
            raise ValueError("Username already exists")

        user = User(
            id=uuid4(),
            username=data.username,
            email=data.email,
            hashed_password=hash_password(data.password),
        )
        created = await self.repo.create(user)
        return UserRead.model_validate(created)

    async def login(self, data: LoginRequest) -> Token:
        user = await self.repo.get_by_username(data.username)
        if not user or not verify_password(data.password, user.hashed_password):
            raise ValueError("Invalid credentials")

        access_token = create_access_token(data={"sub": user.username})
        return Token(access_token=access_token, token_type="bearer")
