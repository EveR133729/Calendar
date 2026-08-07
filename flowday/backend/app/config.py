from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Приложение
    app_name: str = "Flowday API"
    app_version: str = "0.1.0"
    debug: bool = True
    
    # База данных
    database_url: str = "sqlite+aiosqlite:///./flowday.db"
    
    # CORS
    cors_origins: list[str] = [
        "http://localhost:5173",  # Vite dev server
        "http://localhost:1420",  # Tauri dev
        "tauri://localhost",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
