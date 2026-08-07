from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.task_service import ProjectService, TagService
from app.schemas.task import (
    ProjectResponse, ProjectCreate, ProjectUpdate,
    TagResponse, TagCreate, TagUpdate,
)

router = APIRouter()


# ===== Projects =====
@router.get("/projects", response_model=list[ProjectResponse], tags=["Projects"])
async def get_projects(db: AsyncSession = Depends(get_db)):
    """Получить все проекты"""
    service = ProjectService(db)
    projects = await service.get_all()
    return projects


@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED, tags=["Projects"])
async def create_project(project_data: ProjectCreate, db: AsyncSession = Depends(get_db)):
    """Создать новый проект"""
    service = ProjectService(db)
    project = await service.create(project_data)
    return project


@router.get("/projects/{project_id}", response_model=ProjectResponse, tags=["Projects"])
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    """Получить проект по ID"""
    service = ProjectService(db)
    project = await service.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/projects/{project_id}", response_model=ProjectResponse, tags=["Projects"])
async def update_project(project_id: int, project_data: ProjectUpdate, db: AsyncSession = Depends(get_db)):
    """Обновить проект"""
    service = ProjectService(db)
    project = await service.update(project_id, project_data)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Projects"])
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db)):
    """Удалить проект"""
    service = ProjectService(db)
    success = await service.delete(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")


# ===== Tags =====
@router.get("/tags", response_model=list[TagResponse], tags=["Tags"])
async def get_tags(db: AsyncSession = Depends(get_db)):
    """Получить все теги"""
    service = TagService(db)
    tags = await service.get_all()
    return tags


@router.post("/tags", response_model=TagResponse, status_code=status.HTTP_201_CREATED, tags=["Tags"])
async def create_tag(tag_data: TagCreate, db: AsyncSession = Depends(get_db)):
    """Создать новый тег"""
    service = TagService(db)
    tag = await service.create(tag_data)
    return tag


@router.put("/tags/{tag_id}", response_model=TagResponse, tags=["Tags"])
async def update_tag(tag_id: int, tag_data: TagUpdate, db: AsyncSession = Depends(get_db)):
    """Обновить тег"""
    service = TagService(db)
    tag = await service.update(tag_id, tag_data)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.delete("/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tags"])
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    """Удалить тег"""
    service = TagService(db)
    success = await service.delete(tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tag not found")
