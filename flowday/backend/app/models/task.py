from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Integer, Boolean, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
import enum

from app.database import Base


class TaskStatus(str, enum.Enum):
    """Статус задачи"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Priority(str, enum.Enum):
    """Приоритет задачи"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Project(Base):
    """Проект/Категория"""
    __tablename__ = "projects"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    color: Mapped[str] = mapped_column(String(7), default="#3B82F6")  # hex цвет
    icon: Mapped[str] = mapped_column(String(50), default="folder")
    
    # Связи
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="project", cascade="all, delete-orphan")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}')>"


class Task(Base):
    """Задача"""
    __tablename__ = "tasks"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus), 
        default=TaskStatus.PENDING,
        nullable=False
    )
    priority: Mapped[Priority] = mapped_column(
        SQLEnum(Priority), 
        default=Priority.MEDIUM,
        nullable=False
    )
    
    due_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    
    order: Mapped[int] = mapped_column(Integer, default=0)
    
    # Внешние ключи
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id", ondelete="SET NULL"), nullable=True)
    parent_task_id: Mapped[int | None] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), nullable=True)
    
    # Связи
    project = relationship("Project", back_populates="tasks")
    parent_task = relationship("Task", remote_side=[id], backref="subtasks")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status={self.status})>"


class Event(Base):
    """Событие календаря"""
    __tablename__ = "events"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    all_day: Mapped[bool] = mapped_column(Boolean, default=False)
    
    location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    
    # Внешние ключи
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id", ondelete="SET NULL"), nullable=True)
    
    # Связи
    project = relationship("Project", back_populates="events")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Event(id={self.id}, title='{self.title}', start={self.start_time})>"


class Tag(Base):
    """Тег"""
    __tablename__ = "tags"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    color: Mapped[str] = mapped_column(String(7), default="#6B7280")
    
    # Связи многие-ко-многим с задачами
    tasks = relationship("Task", secondary="task_tags", back_populates="tags")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}')>"


class TaskTag(Base):
    """Связь задач и тегов (многие-ко-многим)"""
    __tablename__ = "task_tags"
    
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)


# Добавляем связь tags в модель Task
Task.tags = relationship("Tag", secondary="task_tags", back_populates="tasks")
