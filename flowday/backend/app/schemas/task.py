from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

from app.models.task import TaskStatus, Priority


# Project Schemas
class ProjectBase(BaseModel):
    """Базовая схема проекта"""
    name: str = Field(..., min_length=1, max_length=100)
    color: str = Field(default="#3B82F6", pattern="^#[0-9A-Fa-f]{6}$")
    icon: str = Field(default="folder", max_length=50)


class ProjectCreate(ProjectBase):
    """Схема создания проекта"""
    pass


class ProjectUpdate(BaseModel):
    """Схема обновления проекта (все поля опциональны)"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")
    icon: Optional[str] = Field(None, max_length=50)


class ProjectResponse(ProjectBase):
    """Схема ответа проекта"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Task Schemas
class TaskBase(BaseModel):
    """Базовая схема задачи"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=5000)
    priority: Priority = Field(default=Priority.MEDIUM)
    due_date: Optional[datetime] = None
    project_id: Optional[int] = None
    parent_task_id: Optional[int] = None
    order: int = Field(default=0)


class TaskCreate(TaskBase):
    """Схема создания задачи"""
    pass


class TaskUpdate(BaseModel):
    """Схема обновления задачи (все поля опциональны)"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=5000)
    status: Optional[TaskStatus] = None
    priority: Optional[Priority] = None
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    project_id: Optional[int] = None
    parent_task_id: Optional[int] = None
    order: Optional[int] = None


class TaskResponse(TaskBase):
    """Схема ответа задачи"""
    id: int
    status: TaskStatus
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    # Вложенные данные (опционально, для избежания проблем с lazy loading)
    project: Optional[ProjectResponse] = None
    
    class Config:
        from_attributes = True


class TaskCompleteResponse(BaseModel):
    """Схема ответа после завершения задачи"""
    id: int
    status: TaskStatus
    completed_at: datetime


# Event Schemas
class EventBase(BaseModel):
    """Базовая схема события"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=5000)
    start_time: datetime
    end_time: datetime
    all_day: bool = Field(default=False)
    location: Optional[str] = Field(None, max_length=200)
    project_id: Optional[int] = None


class EventCreate(EventBase):
    """Схема создания события"""
    pass


class EventUpdate(BaseModel):
    """Схема обновления события (все поля опциональны)"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=5000)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    all_day: Optional[bool] = None
    location: Optional[str] = Field(None, max_length=200)
    project_id: Optional[int] = None


class EventResponse(EventBase):
    """Схема ответа события"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    # Вложенные данные
    project: Optional[ProjectResponse] = None
    
    class Config:
        from_attributes = True


# Tag Schemas
class TagBase(BaseModel):
    """Базовая схема тега"""
    name: str = Field(..., min_length=1, max_length=50)
    color: str = Field(default="#6B7280", pattern="^#[0-9A-Fa-f]{6}$")


class TagCreate(TagBase):
    """Схема создания тега"""
    pass


class TagUpdate(BaseModel):
    """Схема обновления тега (все поля опциональны)"""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")


class TagResponse(TagBase):
    """Схема ответа тега"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Health Check
class HealthResponse(BaseModel):
    """Схема ответа health check"""
    status: str
    version: str
    database: str
