from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class UserCreate(BaseModel):
    username: str = Field(
        ...,
        title="Username",
        description="Unique username for the user. Required.",
        min_length=1,
        max_length=50,
    )
    email: str = Field(
        ...,
        title="Email",
        description="Email address of the user. Required.",
    )
    password: str = Field(
        ...,
        title="Password",
        description="Password for the user. Required.",
        min_length=6,
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "password": "secret123",
            }
        }
    }


class UserRead(BaseModel):
    id: UUID = Field(..., title="ID")
    username: str = Field(...)
    email: str = Field(...)

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "username": "john_doe",
                "email": "john@example.com",
            }
        },
    }


class LoginRequest(BaseModel):
    username: str = Field(
        ...,
        title="Username",
        description="Username of the user.",
    )
    password: str = Field(
        ...,
        title="Password",
        description="Password of the user.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {"username": "john_doe", "password": "secret123"}
        }
    }


class Token(BaseModel):
    access_token: str = Field(
        ...,
        title="Access Token",
        description="JWT access token for authentication.",
    )
    token_type: str = Field(
        ...,
        title="Token Type",
        description="Type of the token (typically 'bearer').",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIs...",
                "token_type": "bearer",
            }
        }
    }


class TokenPayload(BaseModel):
    sub: str = Field(...)
    exp: Optional[int] = Field(None)
