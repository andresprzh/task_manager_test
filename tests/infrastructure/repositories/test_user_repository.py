import uuid

import pytest

from task_manager.domain.models import User
from task_manager.infrastructure.repositories import SQLAlchemyUserRepository


@pytest.mark.anyio
async def test_user_repository_create(session_maker):
    """Test creating a user in the repository."""
    user_repo = SQLAlchemyUserRepository(session_maker)

    user_id = uuid.uuid4()
    user = User(
        id=user_id,
        username="john_doe",
        email="john@example.com",
        hashed_password="hashed_secure_password",
    )

    created_user = await user_repo.create(user)

    assert created_user.id == user_id
    assert created_user.username == "john_doe"
    assert created_user.email == "john@example.com"
    assert created_user.hashed_password == "hashed_secure_password"


@pytest.mark.anyio
async def test_user_repository_get(session_maker):
    """Test retrieving a user by ID."""
    user_repo = SQLAlchemyUserRepository(session_maker)

    user_id = uuid.uuid4()
    user = User(
        id=user_id,
        username="alice",
        email="alice@example.com",
        hashed_password="hash_alice",
    )
    await user_repo.create(user)

    fetched_user = await user_repo.get(user_id)

    assert fetched_user is not None
    assert fetched_user.id == user_id
    assert fetched_user.username == "alice"
    assert fetched_user.email == "alice@example.com"


@pytest.mark.anyio
async def test_user_repository_get_missing(session_maker):
    """Test retrieving a non-existent user returns None."""
    user_repo = SQLAlchemyUserRepository(session_maker)

    missing_id = uuid.uuid4()
    fetched_user = await user_repo.get(missing_id)

    assert fetched_user is None


@pytest.mark.anyio
async def test_user_repository_get_by_username(session_maker):
    """Test retrieving a user by username."""
    user_repo = SQLAlchemyUserRepository(session_maker)

    user_id = uuid.uuid4()
    user = User(
        id=user_id,
        username="bob_smith",
        email="bob@example.com",
        hashed_password="hash_bob",
    )
    await user_repo.create(user)

    fetched_user = await user_repo.get_by_username("bob_smith")

    assert fetched_user is not None
    assert fetched_user.id == user_id
    assert fetched_user.username == "bob_smith"
    assert fetched_user.email == "bob@example.com"


@pytest.mark.anyio
async def test_user_repository_get_by_username_not_found(session_maker):
    """Test retrieving by non-existent username returns None."""
    user_repo = SQLAlchemyUserRepository(session_maker)

    fetched_user = await user_repo.get_by_username("nonexistent_user")

    assert fetched_user is None


@pytest.mark.anyio
async def test_user_repository_multiple_users(session_maker):
    """Test creating and retrieving multiple users."""
    user_repo = SQLAlchemyUserRepository(session_maker)

    users_data = [
        ("user1", "user1@example.com", "hash1"),
        ("user2", "user2@example.com", "hash2"),
        ("user3", "user3@example.com", "hash3"),
    ]

    created_ids = []
    for username, email, hashed_pwd in users_data:
        user = User(
            id=uuid.uuid4(),
            username=username,
            email=email,
            hashed_password=hashed_pwd,
        )
        created_user = await user_repo.create(user)
        created_ids.append(created_user.id)

    # Verify all users can be retrieved by username
    for username, _, _ in users_data:
        fetched_user = await user_repo.get_by_username(username)
        assert fetched_user is not None
        assert fetched_user.username == username

    # Verify all users can be retrieved by ID
    for user_id in created_ids:
        fetched_user = await user_repo.get(user_id)
        assert fetched_user is not None
        assert fetched_user.id == user_id


@pytest.mark.anyio
async def test_user_repository_unique_username(session_maker):
    """Test that unique username constraint is enforced."""
    user_repo = SQLAlchemyUserRepository(session_maker)

    user1 = User(
        id=uuid.uuid4(),
        username="unique_user",
        email="user1@example.com",
        hashed_password="hash1",
    )
    await user_repo.create(user1)

    # Attempting to create another user with same username should fail
    user2 = User(
        id=uuid.uuid4(),
        username="unique_user",
        email="user2@example.com",
        hashed_password="hash2",
    )

    with pytest.raises(Exception):  # SQLAlchemy integrity error
        await user_repo.create(user2)


@pytest.mark.anyio
async def test_user_repository_unique_email(session_maker):
    """Test that unique email constraint is enforced."""
    user_repo = SQLAlchemyUserRepository(session_maker)

    user1 = User(
        id=uuid.uuid4(),
        username="user1",
        email="unique@example.com",
        hashed_password="hash1",
    )
    await user_repo.create(user1)

    # Attempting to create another user with same email should fail
    user2 = User(
        id=uuid.uuid4(),
        username="user2",
        email="unique@example.com",
        hashed_password="hash2",
    )

    with pytest.raises(Exception):  # SQLAlchemy integrity error
        await user_repo.create(user2)
