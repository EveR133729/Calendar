# Flowday - Архитектурная документация

## 1. Структура проекта

```
flowday/
├── backend/                    # FastAPI + Python
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # Точка входа FastAPI
│   │   ├── config.py          # Конфигурация приложения
│   │   ├── database.py        # Подключение к SQLite
│   │   ├── models/            # SQLAlchemy модели
│   │   │   ├── __init__.py
│   │   │   ├── task.py
│   │   │   ├── event.py
│   │   │   ├── project.py
│   │   │   └── user.py
│   │   ├── schemas/           # Pydantic схемы для API
│   │   │   ├── __init__.py
│   │   │   ├── task.py
│   │   │   ├── event.py
│   │   │   ├── project.py
│   │   │   └── user.py
│   │   ├── routers/           # API роутеры
│   │   │   ├── __init__.py
│   │   │   ├── tasks.py
│   │   │   ├── events.py
│   │   │   ├── projects.py
│   │   │   └── users.py
│   │   └── services/          # Бизнес-логика
│   │       ├── __init__.py
│   │       ├── task_service.py
│   │       ├── event_service.py
│   │       └── project_service.py
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
│
├── frontend/                   # React + TypeScript + Tauri
│   ├── src/
│   │   ├── components/        # Переиспользуемые UI компоненты
│   │   │   ├── ui/           # Базовые компоненты (Button, Input, etc.)
│   │   │   ├── layout/       # Layout компоненты
│   │   │   └── common/       # Общие компоненты
│   │   ├── features/         # Фичи по доменам
│   │   │   ├── tasks/
│   │   │   ├── events/
│   │   │   ├── projects/
│   │   │   └── calendar/
│   │   ├── hooks/            # Кастомные хуки
│   │   ├── lib/              # Утилиты, API клиент, валидация
│   │   │   ├── api.ts        # API клиент
│   │   │   ├── utils.ts
│   │   │   └── validations.ts # Zod схемы
│   │   ├── store/            # Zustand сторы
│   │   │   ├── index.ts
│   │   │   ├── taskStore.ts
│   │   │   ├── eventStore.ts
│   │   │   └── uiStore.ts
│   │   ├── types/            # TypeScript типы
│   │   │   ├── index.ts
│   │   │   ├── task.ts
│   │   │   ├── event.ts
│   │   │   └── project.ts
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css         # Tailwind директивы
│   ├── public/
│   ├── src-tauri/           # Tauri специфичный код
│   ├── package.json
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── README.md
│
└── README.md                # Общая документация проекта
```

## 2. Архитектура Frontend

### Компонентная архитектура
- **UI Components** (`src/components/ui/`): Атомарные переиспользуемые компоненты (Button, Input, Card, Modal)
- **Layout Components** (`src/components/layout/`): Структурные компоненты (Sidebar, Header, MainLayout)
- **Feature Components** (`src/features/*/`): Компоненты, специфичные для доменов (TaskList, EventCard, ProjectView)

### State Management (Zustand)
Разделение сторов по доменам:
- `taskStore`: Управление задачами (CRUD, фильтрация, сортировка)
- `eventStore`: Управление событиями календаря
- `projectStore`: Управление проектами/категориями
- `uiStore`: UI состояние (темы, модальные окна, сайдбар)

Преимущества Zustand:
- Минимальный ботерплейт
- TypeScript из коробки
- Легкая тестируемость
- Отсутствие провайдеров (в отличие от Redux Context)

### API Client
Единый клиент для взаимодействия с backend через fetch/axios с типизацией ответов.

### Валидация форм (Zod)
Схемы валидации для форм создания/редактирования задач и событий.

## 3. Архитектура Backend

### Слои архитектуры
1. **Routers** (`app/routers/`): HTTP endpoints, валидация входящих данных
2. **Services** (`app/services/`): Бизнес-логика, оркестрация операций
3. **Models** (`app/models/`): SQLAlchemy ORM модели
4. **Schemas** (`app/schemas/`): Pydantic схемы для request/response

### Преимущества такого разделения
- Четкое разделение ответственности
- Легкость тестирования каждого слоя
- Возможность замены ORM без изменения бизнес-логики
- Переиспользование сервисов в разных контекстах

## 4. Основные сущности базы данных

### User (Пользователь)
```sql
- id: INTEGER PRIMARY KEY
- email: VARCHAR UNIQUE
- username: VARCHAR
- created_at: DATETIME
- updated_at: DATETIME
```

### Project (Проект/Категория)
```sql
- id: INTEGER PRIMARY KEY
- name: VARCHAR NOT NULL
- color: VARCHAR (hex цвет для визуализации)
- icon: VARCHAR (идентификатор иконки Lucide)
- user_id: INTEGER FOREIGN KEY
- created_at: DATETIME
- updated_at: DATETIME
```

### Task (Задача)
```sql
- id: INTEGER PRIMARY KEY
- title: VARCHAR NOT NULL
- description: TEXT
- status: ENUM (pending, in_progress, completed, cancelled)
- priority: ENUM (low, medium, high, urgent)
- due_date: DATETIME
- completed_at: DATETIME
- project_id: INTEGER FOREIGN KEY
- parent_task_id: INTEGER FOREIGN KEY (для подзадач)
- order: INTEGER (для сортировки)
- created_at: DATETIME
- updated_at: DATETIME
```

### Event (Событие календаря)
```sql
- id: INTEGER PRIMARY KEY
- title: VARCHAR NOT NULL
- description: TEXT
- start_time: DATETIME NOT NULL
- end_time: DATETIME NOT NULL
- all_day: BOOLEAN
- location: VARCHAR
- project_id: INTEGER FOREIGN KEY
- user_id: INTEGER FOREIGN KEY
- created_at: DATETIME
- updated_at: DATETIME
```

### Tag (Тег)
```sql
- id: INTEGER PRIMARY KEY
- name: VARCHAR NOT NULL
- color: VARCHAR
- user_id: INTEGER FOREIGN KEY
```

### TaskTag (Связь многие-ко-многим Task-Tag)
```sql
- task_id: INTEGER FOREIGN KEY
- tag_id: INTEGER FOREIGN KEY
- PRIMARY KEY (task_id, tag_id)
```

## 5. API Endpoints

### Authentication (будущее расширение)
- `POST /api/v1/auth/register` - Регистрация
- `POST /api/v1/auth/login` - Логин
- `POST /api/v1/auth/logout` - Логаут
- `GET /api/v1/auth/me` - Текущий пользователь

### Tasks
- `GET /api/v1/tasks` - Список задач (с фильтрацией, сортировкой, пагинацией)
- `GET /api/v1/tasks/{id}` - Получить задачу по ID
- `POST /api/v1/tasks` - Создать задачу
- `PUT /api/v1/tasks/{id}` - Обновить задачу
- `PATCH /api/v1/tasks/{id}/complete` - Отметить как выполненную
- `DELETE /api/v1/tasks/{id}` - Удалить задачу
- `GET /api/v1/tasks/{id}/subtasks` - Получить подзадачи

### Events
- `GET /api/v1/events` - Список событий (с фильтрацией по датам)
- `GET /api/v1/events/{id}` - Получить событие по ID
- `POST /api/v1/events` - Создать событие
- `PUT /api/v1/events/{id}` - Обновить событие
- `DELETE /api/v1/events/{id}` - Удалить событие
- `GET /api/v1/events/calendar/{start}/{end}` - События для диапазона дат

### Projects
- `GET /api/v1/projects` - Список проектов
- `GET /api/v1/projects/{id}` - Получить проект по ID
- `POST /api/v1/projects` - Создать проект
- `PUT /api/v1/projects/{id}` - Обновить проект
- `DELETE /api/v1/projects/{id}` - Удалить проект
- `GET /api/v1/projects/{id}/tasks` - Задачи проекта
- `GET /api/v1/projects/{id}/events` - События проекта

### Tags
- `GET /api/v1/tags` - Список тегов
- `POST /api/v1/tags` - Создать тег
- `PUT /api/v1/tags/{id}` - Обновить тег
- `DELETE /api/v1/tags/{id}` - Удалить тег

### Health Check
- `GET /api/v1/health` - Проверка здоровья API

## 6. Система маршрутизации (Frontend)

### Основные роуты
```
/ - Dashboard (сегодняшние задачи и события)
/tasks - Все задачи
/tasks/:id - Детали задачи
/calendar - Календарь (месяц/неделя/день)
/projects - Список проектов
/projects/:id - Детали проекта
/settings - Настройки приложения
```

### Роутинг реализован через React Router v6+
- Ленивая загрузка компонентов (lazy loading)
- Защищенные роуты (после добавления авторизации)
- Параметризированные роуты для деталей сущностей

## 7. Объяснение архитектурных решений

### Почему Tauri вместо Electron?
- Меньший размер бандла (~10MB vs ~150MB)
- Лучшая производительность (использует системный WebView)
- Rust backend для нативных функций
- Безопасность по умолчанию

### Почему SQLite на первом этапе?
- Zero configuration
- Портативность (один файл)
- Достаточно для локального использования
- Легкая миграция на PostgreSQL при необходимости синхронизации

### Почему Zustand вместо Redux?
- В 3 раза меньше кода
- Нет необходимости в провайдерах
- Отличная TypeScript поддержка
- Встроенная персистентность (через middleware)

### Почему модульная структура features?
- Каждый feature самодостаточен
- Легкое удаление/добавление функциональности
- Упрощенное тестирование
- Масштабируемость для мобильной версии

### Разделение API по версиям (/api/v1/)
- Возможность бесшовного обновления API
- Обратная совместимость
- Подготовка к будущей синхронизации

## 8. План развития

### Этап 1 (сейчас)
- ✅ Skeleton проекта
- ✅ Базовая структура БД
- ✅ Минимальные API endpoints
- ✅ Базовый UI

### Этап 2 (следующий)
- CRUD для задач
- CRUD для проектов
- Интеграция frontend ↔ backend

### Этап 3
- Календарь (месяц/неделя/день views)
- Drag-and-drop для задач
- Подзадачи и чеклисты

### Этап 4
- Теги и фильтрация
- Поиск
- Повторяющиеся задачи

### Этап 5
- Синхронизация (PostgreSQL + WebSocket)
- Мобильная версия (React Native или Tauri Mobile)
- Уведомления
