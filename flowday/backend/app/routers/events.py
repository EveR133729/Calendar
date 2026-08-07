from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.task_service import EventService
from app.schemas.task import EventResponse, EventCreate, EventUpdate

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("", response_model=list[EventResponse])
async def get_events(
    db: AsyncSession = Depends(get_db),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    project_id: Optional[int] = None,
):
    """Получить все события с фильтрацией по датам"""
    service = EventService(db)
    events = await service.get_all(
        start_date=start_date,
        end_date=end_date,
        project_id=project_id,
    )
    return events


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    event_data: EventCreate,
    db: AsyncSession = Depends(get_db),
):
    """Создать новое событие"""
    service = EventService(db)
    event = await service.create(event_data)
    return event


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Получить событие по ID"""
    service = EventService(db)
    event = await service.get_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.put("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: int,
    event_data: EventUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Обновить событие"""
    service = EventService(db)
    event = await service.update(event_id, event_data)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Удалить событие"""
    service = EventService(db)
    success = await service.delete(event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event not found")


@router.get("/calendar/{start}/{end}", response_model=list[EventResponse])
async def get_calendar_events(
    start: str,
    end: str,
    db: AsyncSession = Depends(get_db),
):
    """Получить события для диапазона дат (формат: YYYY-MM-DD)"""
    try:
        start_date = datetime.fromisoformat(start)
        end_date = datetime.fromisoformat(end)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    service = EventService(db)
    events = await service.get_all(
        start_date=start_date,
        end_date=end_date,
    )
    return events
