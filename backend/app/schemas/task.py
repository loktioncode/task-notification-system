from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "pending"
    priority: Optional[str] = "medium"
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    assigned_to_id: Optional[int] = None

class TaskUpdate(TaskBase):
    title: Optional[str] = None
    assigned_to_id: Optional[int] = None
    completed_at: Optional[datetime] = None

class TaskStatusUpdate(BaseModel):
    status: str

class TaskInDBBase(TaskBase):
    id: int
    owner_id: int
    assigned_to_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Task(TaskInDBBase):
    pass