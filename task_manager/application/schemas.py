from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class TaskCreate(BaseModel):
    title: str = Field(..., title="Title", example="Buy groceries")
    description: Optional[str] = Field(
        None, title="Description", example="Milk, eggs, bread"
    )


class TaskRead(BaseModel):
    id: UUID = Field(..., title="ID", example="3fa85f64-5717-4562-b3fc-2c963f66afa6")
    title: str = Field(..., example="Buy groceries")
    description: Optional[str] = Field(None, example="Milk, eggs, bread")
    completed: bool = Field(False, example=False)
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
            }
        },
    }
