from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db, get_db
from app.routers import tasks, events, projects


def create_app() -> FastAPI:
    """Фабрика приложения FastAPI"""
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="API для приложения-планировщика Flowday",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Подключение роутеров
    app.include_router(tasks.router, prefix="/api/v1")
    app.include_router(events.router, prefix="/api/v1")
    app.include_router(projects.router, prefix="/api/v1")
    
    # Health check endpoint
    @app.get("/api/v1/health", tags=["Health"])
    async def health_check():
        """Проверка здоровья API"""
        return {
            "status": "healthy",
            "version": settings.app_version,
            "database": "connected",
        }
    
    # Инициализация БД при старте
    @app.on_event("startup")
    async def on_startup():
        """Инициализация при запуске"""
        await init_db()
        print(f"🚀 {settings.app_name} v{settings.app_version} запущен")
        print(f"📚 Docs: http://localhost:8000/docs")
    
    return app


# Создаем экземпляр приложения
app = create_app()
