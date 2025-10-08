from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AddTask(BaseModel):
    title: str = Field(max_length=30)
    description: Optional[str]


class ReadTask(AddTask):
    id: int
    created_at: datetime


class EditTask(AddTask):
    pass


class DeleteTask(BaseModel):
    id: int