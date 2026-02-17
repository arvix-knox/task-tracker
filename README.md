# Task Tracker

Backend-основа для трекера задач на Python: конфигурация, подключение к PostgreSQL, модели данных и Alembic-миграции.

На текущем этапе в репозитории **нет** готовой точки входа FastAPI (`main.py`) и HTTP-эндпоинтов. Проект сейчас находится на стадии подготовки доменной модели и схем БД.

## Что реализовано

- асинхронное подключение к PostgreSQL через SQLAlchemy 2.0 (`asyncpg`);
- модели `User` и `Task`;
- Pydantic-схемы для создания/обновления/ответов;
- Alembic-конфигурация и первая миграция создания таблиц.

## Стек

- Python 3.12+
- SQLAlchemy 2.0 (async)
- Alembic
- Pydantic v2
- PostgreSQL

## Структура проекта

```text
.
├── app
│   ├── config.py         # настройки из .env
│   ├── db
│   │   ├── base.py       # Declarative Base
│   │   └── session.py    # async engine + session factory
│   ├── models
│   │   ├── user.py
│   │   └── task.py
│   └── schemas
│       ├── user.py
│       └── task.py
├── alembic
│   ├── env.py
│   └── versions
└── alembic.ini
```

## Быстрый старт

1. Создайте и активируйте виртуальное окружение:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Подготовьте `.env`:

```bash
cp .env.example .env
```

4. Создайте базу данных и включите расширение `pgcrypto` (нужно для `gen_random_uuid()`):

```bash
psql -U postgres -c "CREATE DATABASE task_tracker;"
psql -U postgres -d task_tracker -c "CREATE EXTENSION IF NOT EXISTS pgcrypto;"
```

5. Примените миграции:

```bash
alembic upgrade head
```

## Переменные окружения

Пример в файле `.env.example`.

- `DATABASE_URL` - строка подключения к PostgreSQL (async), пример:
  `postgresql+asyncpg://postgres:password@localhost:5432/task_tracker`
- `SECRET_KEY` - секрет для подписи токенов (рекомендуется 32+ байт в hex)
- `ALGORITHM` - алгоритм подписи JWT (по умолчанию `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - время жизни access token
- `REFRESH_TOKEN_EXPIRE_DAYS` - время жизни refresh token
- `APP_NAME` - имя приложения
- `DEBUG` - режим отладки (`true`/`false`)

## Команды Alembic

Создать новую миграцию из изменений моделей:

```bash
alembic revision --autogenerate -m "describe change"
```

Откатить последнюю миграцию:

```bash
alembic downgrade -1
```

## Текущее ограничение

HTTP API, роуты, сервисы и репозитории пока не реализованы. Следующий шаг развития проекта - добавить FastAPI-приложение и CRUD-эндпоинты для пользователей и задач.
