from datetime import datetime
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.task import Project, Task, Event, Tag, TaskTag, TaskStatus
from app.schemas.task import (
    ProjectCreate, ProjectUpdate,
    TaskCreate, TaskUpdate,
    EventCreate, EventUpdate,
    TagCreate, TagUpdate,
)


class ProjectService:
    """Сервис для работы с проектами"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(self) -> list[Project]:
        """Получить все проекты"""
        result = await self.db.execute(select(Project).order_by(Project.name))
        return list(result.scalars().all())
    
    async def get_by_id(self, project_id: int) -> Optional[Project]:
        """Получить проект по ID"""
        result = await self.db.execute(
            select(Project)
            .options(selectinload(Project.tasks), selectinload(Project.events))
            .where(Project.id == project_id)
        )
        return result.scalar_one_or_none()
    
    async def create(self, project_data: ProjectCreate) -> Project:
        """Создать проект"""
        project = Project(**project_data.model_dump())
        self.db.add(project)
        await self.db.flush()
        await self.db.refresh(project)
        return project
    
    async def update(self, project_id: int, project_data: ProjectUpdate) -> Optional[Project]:
        """Обновить проект"""
        project = await self.get_by_id(project_id)
        if not project:
            return None
        
        update_data = project_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)
        
        project.updated_at = datetime.utcnow()
        await self.db.flush()
        await self.db.refresh(project)
        return project
    
    async def delete(self, project_id: int) -> bool:
        """Удалить проект"""
        project = await self.get_by_id(project_id)
        if not project:
            return False
        
        await self.db.delete(project)
        await self.db.flush()
        return True


class TaskService:
    """Сервис для работы с задачами"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(
        self, 
        status: Optional[TaskStatus] = None,
        project_id: Optional[int] = None,
        priority: Optional[str] = None,
    ) -> list[Task]:
        """Получить все задачи с фильтрацией"""
        query = select(Task).options(
            selectinload(Task.project),
            selectinload(Task.subtasks),
            selectinload(Task.tags)
        ).order_by(Task.order, Task.created_at)
        
        if status:
            query = query.where(Task.status == status)
        if project_id:
            query = query.where(Task.project_id == project_id)
        if priority:
            query = query.where(Task.priority == priority)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_by_id(self, task_id: int) -> Optional[Task]:
        """Получить задачу по ID"""
        result = await self.db.execute(
            select(Task)
            .options(
                selectinload(Task.project),
                selectinload(Task.subtasks),
                selectinload(Task.tags)
            )
            .where(Task.id == task_id)
        )
        return result.scalar_one_or_none()
    
    async def create(self, task_data: TaskCreate) -> Task:
        """Создать задачу"""
        task = Task(**task_data.model_dump())
        self.db.add(task)
        await self.db.flush()
        await self.db.refresh(task)
        return task
    
    async def update(self, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
        """Обновить задачу"""
        task = await self.get_by_id(task_id)
        if not task:
            return None
        
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        
        # Автозаполнение completed_at при изменении статуса
        if task_data.status == TaskStatus.COMPLETED and not task.completed_at:
            task.completed_at = datetime.utcnow()
        elif task_data.status != TaskStatus.COMPLETED:
            task.completed_at = None
        
        task.updated_at = datetime.utcnow()
        await self.db.flush()
        await self.db.refresh(task)
        return task
    
    async def complete(self, task_id: int) -> Optional[Task]:
        """Отметить задачу как выполненную"""
        task = await self.get_by_id(task_id)
        if not task:
            return None
        
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.utcnow()
        task.updated_at = datetime.utcnow()
        
        await self.db.flush()
        await self.db.refresh(task)
        return task
    
    async def delete(self, task_id: int) -> bool:
        """Удалить задачу"""
        task = await self.get_by_id(task_id)
        if not task:
            return False
        
        await self.db.delete(task)
        await self.db.flush()
        return True


class EventService:
    """Сервис для работы с событиями"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        project_id: Optional[int] = None,
    ) -> list[Event]:
        """Получить все события с фильтрацией по датам"""
        query = select(Event).options(
            selectinload(Event.project)
        ).order_by(Event.start_time)
        
        if start_date:
            query = query.where(Event.end_time >= start_date)
        if end_date:
            query = query.where(Event.start_time <= end_date)
        if project_id:
            query = query.where(Event.project_id == project_id)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_by_id(self, event_id: int) -> Optional[Event]:
        """Получить событие по ID"""
        result = await self.db.execute(
            select(Event)
            .options(selectinload(Event.project))
            .where(Event.id == event_id)
        )
        return result.scalar_one_or_none()
    
    async def create(self, event_data: EventCreate) -> Event:
        """Создать событие"""
        event = Event(**event_data.model_dump())
        self.db.add(event)
        await self.db.flush()
        await self.db.refresh(event)
        return event
    
    async def update(self, event_id: int, event_data: EventUpdate) -> Optional[Event]:
        """Обновить событие"""
        event = await self.get_by_id(event_id)
        if not event:
            return None
        
        update_data = event_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(event, field, value)
        
        event.updated_at = datetime.utcnow()
        await self.db.flush()
        await self.db.refresh(event)
        return event
    
    async def delete(self, event_id: int) -> bool:
        """Удалить событие"""
        event = await self.get_by_id(event_id)
        if not event:
            return False
        
        await self.db.delete(event)
        await self.db.flush()
        return True


class TagService:
    """Сервис для работы с тегами"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(self) -> list[Tag]:
        """Получить все теги"""
        result = await self.db.execute(select(Tag).order_by(Tag.name))
        return list(result.scalars().all())
    
    async def get_by_id(self, tag_id: int) -> Optional[Tag]:
        """Получить тег по ID"""
        result = await self.db.execute(
            select(Tag).where(Tag.id == tag_id)
        )
        return result.scalar_one_or_none()
    
    async def create(self, tag_data: TagCreate) -> Tag:
        """Создать тег"""
        tag = Tag(**tag_data.model_dump())
        self.db.add(tag)
        await self.db.flush()
        await self.db.refresh(tag)
        return tag
    
    async def update(self, tag_id: int, tag_data: TagUpdate) -> Optional[Tag]:
        """Обновить тег"""
        tag = await self.get_by_id(tag_id)
        if not tag:
            return None
        
        update_data = tag_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(tag, field, value)
        
        tag.updated_at = datetime.utcnow()
        await self.db.flush()
        await self.db.refresh(tag)
        return tag
    
    async def delete(self, tag_id: int) -> bool:
        """Удалить тег"""
        tag = await self.get_by_id(tag_id)
        if not tag:
            return False
        
        await self.db.delete(tag)
        await self.db.flush()
        return True
