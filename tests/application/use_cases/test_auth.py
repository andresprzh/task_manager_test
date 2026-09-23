import pytest

from task_manager.application.use_cases.auth import AuthUseCase
from task_manager.application.schemas.user import UserCreate, LoginRequest
from task_manager.infrastructure.repositories import SQLAlchemyUserRepository


@pytest.mark.anyio
async def test_auth_use_case_register(session_maker):
    """Test registering a new user."""
    user_repo = SQLAlchemyUserRepository(session_maker)
    auth_uc = AuthUseCase(user_repo)

    user_data = UserCreate(
        username="john_doe", email="john@example.com", password="secure_password"
    )

    created_user = await auth_uc.register(user_data)

    assert created_user.username == "john_doe"
    assert created_user.email == "john@example.com"
    assert created_user.id is not None


@pytest.mark.anyio
async def test_auth_use_case_register_duplicate_username(session_maker):
    """Test that registering with duplicate username raises error."""
    user_repo = SQLAlchemyUserRepository(session_maker)
    auth_uc = AuthUseCase(user_repo)

    user_data = UserCreate(
        username="alice", email="alice@example.com", password="password1"
    )
    await auth_uc.register(user_data)

    # Attempt to register with same username
    duplicate_data = UserCreate(
        username="alice", email="alice2@example.com", password="password2"
    )

    with pytest.raises(ValueError, match="Username already exists"):
        await auth_uc.register(duplicate_data)


@pytest.mark.anyio
async def test_auth_use_case_login_valid(session_maker):
    """Test logging in with valid credentials."""
    user_repo = SQLAlchemyUserRepository(session_maker)
    auth_uc = AuthUseCase(user_repo)

    # Register a user first
    user_data = UserCreate(
        username="bob", email="bob@example.com", password="correct_password"
    )
    await auth_uc.register(user_data)

    # Login with correct credentials
    login_data = LoginRequest(username="bob", password="correct_password")
    token_response = await auth_uc.login(login_data)

    assert token_response.access_token is not None
    assert token_response.token_type == "bearer"
    assert len(token_response.access_token) > 0


@pytest.mark.anyio
async def test_auth_use_case_login_invalid_password(session_maker):
    """Test logging in with invalid password."""
    user_repo = SQLAlchemyUserRepository(session_maker)
    auth_uc = AuthUseCase(user_repo)

    # Register a user
    user_data = UserCreate(
        username="charlie", email="charlie@example.com", password="correct_password"
    )
    await auth_uc.register(user_data)

    # Login with wrong password
    login_data = LoginRequest(username="charlie", password="wrong_password")

    with pytest.raises(ValueError, match="Invalid credentials"):
        await auth_uc.login(login_data)


@pytest.mark.anyio
async def test_auth_use_case_login_nonexistent_user(session_maker):
    """Test logging in with non-existent username."""
    user_repo = SQLAlchemyUserRepository(session_maker)
    auth_uc = AuthUseCase(user_repo)

    login_data = LoginRequest(username="nonexistent", password="any_password")

    with pytest.raises(ValueError, match="Invalid credentials"):
        await auth_uc.login(login_data)


@pytest.mark.anyio
async def test_auth_use_case_register_and_login_flow(session_maker):
    """Test complete register and login flow."""
    user_repo = SQLAlchemyUserRepository(session_maker)
    auth_uc = AuthUseCase(user_repo)

    # Register
    register_data = UserCreate(
        username="david", email="david@example.com", password="my_secure_password"
    )
    registered_user = await auth_uc.register(register_data)

    assert registered_user.username == "david"
    assert registered_user.email == "david@example.com"

    # Login
    login_data = LoginRequest(username="david", password="my_secure_password")
    token_response = await auth_uc.login(login_data)

    assert token_response.access_token is not None
    assert token_response.token_type == "bearer"
