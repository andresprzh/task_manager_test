import uuid

import pytest
from pydantic import ValidationError

from task_manager.application.schemas.user import (
    UserCreate,
    UserRead,
    LoginRequest,
    Token,
    TokenPayload,
)


def test_user_create_valid():
    """Test creating a valid UserCreate schema."""
    user_data = UserCreate(
        username="john_doe", email="john@example.com", password="secure_password"
    )

    assert user_data.username == "john_doe"
    assert user_data.email == "john@example.com"
    assert user_data.password == "secure_password"


def test_user_create_missing_required_fields():
    """Test UserCreate with missing required fields."""
    with pytest.raises(ValidationError):
        UserCreate(username="john_doe")

    with pytest.raises(ValidationError):
        UserCreate(email="john@example.com")

    with pytest.raises(ValidationError):
        UserCreate(password="secure_password")


def test_user_create_password_too_short():
    """Test UserCreate with password less than 6 characters."""
    with pytest.raises(ValidationError):
        UserCreate(
            username="john_doe",
            email="john@example.com",
            password="short",
        )


def test_user_read_model():
    """Test UserRead schema."""
    user_id = uuid.uuid4()
    user_data = UserRead(id=user_id, username="john_doe", email="john@example.com")

    assert user_data.id == user_id
    assert user_data.username == "john_doe"
    assert user_data.email == "john@example.com"


def test_login_request_valid():
    """Test creating a valid LoginRequest."""
    login_data = LoginRequest(username="john_doe", password="secure_password")

    assert login_data.username == "john_doe"
    assert login_data.password == "secure_password"


def test_login_request_missing_fields():
    """Test LoginRequest with missing fields."""
    with pytest.raises(ValidationError):
        LoginRequest(username="john_doe")

    with pytest.raises(ValidationError):
        LoginRequest(password="secure_password")


def test_token_model():
    """Test Token schema."""
    token_data = Token(
        access_token="eyJhbGciOiJIUzI1NiIs...",
        token_type="bearer",
    )

    assert token_data.access_token == "eyJhbGciOiJIUzI1NiIs..."
    assert token_data.token_type == "bearer"


def test_token_payload_model():
    """Test TokenPayload schema."""
    payload = TokenPayload(sub="john_doe", exp=1234567890)

    assert payload.sub == "john_doe"
    assert payload.exp == 1234567890


def test_token_payload_without_exp():
    """Test TokenPayload without expiration."""
    payload = TokenPayload(sub="john_doe")

    assert payload.sub == "john_doe"
    assert payload.exp is None


def test_user_create_extra_fields_forbidden():
    """Test that UserCreate forbids extra fields."""
    with pytest.raises(ValidationError):
        UserCreate(
            username="john_doe",
            email="john@example.com",
            password="secure_password",
            extra_field="should_fail",
        )


def test_login_request_extra_fields_forbidden():
    """Test that LoginRequest forbids extra fields."""
    with pytest.raises(ValidationError):
        LoginRequest(
            username="john_doe", password="secure_password", extra="should_fail"
        )
