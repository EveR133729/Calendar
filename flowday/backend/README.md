# Flowday Backend

FastAPI backend для приложения Flowday.

## Установка

```bash
pip install -r requirements.txt
```

## Запуск

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

После запуска документация доступна по адресу:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Структура

```
app/
├── main.py           # Точка входа
├── config.py         # Конфигурация
├── database.py       # Подключение к БД
├── models/           # SQLAlchemy модели
├── schemas/          # Pydantic схемы
├── routers/          # API роутеры
└── services/         # Бизнес-логика
```
