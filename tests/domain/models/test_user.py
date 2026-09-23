import uuid

from task_manager.domain.models import User


def test_user_model_creation():
    """Test creating a User domain model."""
    user_id = uuid.uuid4()
    user = User(
        id=user_id,
        username="john_doe",
        email="john@example.com",
        hashed_password="hashed_pwd_123",
    )

    assert user.id == user_id
    assert user.username == "john_doe"
    assert user.email == "john@example.com"
    assert user.hashed_password == "hashed_pwd_123"


def test_user_model_with_different_data():
    """Test User with different usernames and emails."""
    user1 = User(
        id=uuid.uuid4(),
        username="alice",
        email="alice@example.com",
        hashed_password="hash1",
    )
    user2 = User(
        id=uuid.uuid4(),
        username="bob",
        email="bob@example.com",
        hashed_password="hash2",
    )

    assert user1.username != user2.username
    assert user1.email != user2.email
    assert user1.id != user2.id
