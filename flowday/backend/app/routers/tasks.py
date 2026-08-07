from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.task_service import TaskService, EventService, ProjectService, TagService
from app.schemas.task import (
    TaskResponse, TaskCreate, TaskUpdate, TaskCompleteResponse,
    EventResponse, EventCreate, EventUpdate,
    ProjectResponse, ProjectCreate, ProjectUpdate,
    TagResponse, TagCreate, TagUpdate,
)
from app.models.task import TaskStatus

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", response_model=list[TaskResponse])
async def get_tasks(
    db: AsyncSession = Depends(get_db),
    status_filter: Optional[TaskStatus] = None,
    project_id: Optional[int] = None,
    priority: Optional[str] = None,
):
    """Получить все задачи с фильтрацией"""
    service = TaskService(db)
    tasks = await service.get_all(
        status=status_filter,
        project_id=project_id,
        priority=priority,
    )
    return tasks


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
):
    """Создать новую задачу"""
    service = TaskService(db)
    task = await service.create(task_data)
    return task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Получить задачу по ID"""
    service = TaskService(db)
    task = await service.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Обновить задачу"""
    service = TaskService(db)
    task = await service.update(task_id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}/complete", response_model=TaskCompleteResponse)
async def complete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Отметить задачу как выполненную"""
    service = TaskService(db)
    task = await service.complete(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskCompleteResponse(
        id=task.id,
        status=task.status,
        completed_at=task.completed_at,
    )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Удалить задачу"""
    service = TaskService(db)
    success = await service.delete(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
