Проект Telegram-бота для анализа товародвижения и рекомендаций по закупкам.
Принимает файлы из 1С (CSV/Excel), анализирует остатки и продажи, выдаёт рекомендации.

**Стек:** Python 3.12, aiogram 3, SQLAlchemy 2, Alembic, LiteLLM, UV

---

## Структура проекта

```
domain/                  # Бизнес-логика (не зависит ни от чего)
├── user/                # Пользователь, роли (USER / ADMIN)
├── nomenclature/        # Товары, продажи, остатки, транзиты
└── analysis/            # Запросы на анализ, рекомендации по закупкам

application/             # Use cases — оркестрируют domain
└── use_cases/           # register_user, check_access, manage_user

infrastructure/          # Реализации интерфейсов из domain
├── db/                  # SQLAlchemy ORM, сессия, репозитории
├── llm/                 # Интеграция с LLM через LiteLLM
└── file_parser/         # Парсинг CSV/Excel из 1С

interfaces/              # Точки входа
└── telegram/            # Telegram-бот (aiogram): handlers, middleware

tests/                   # Тесты (зеркалят структуру выше)
migrations/              # Alembic-миграции БД
scripts/                 # Утилиты (add_admin.py и др.)
docker/
├── bot/
│   └── Dockerfile       # Продовый образ (только код приложения, без dev-зависимостей)
└── dev/
    └── Dockerfile       # Dev-образ (код через volume, dev-зависимости для тестов/линтеров)
```

**Главное правило:** `domain/` ничего не импортирует из других слоёв. Зависимости всегда направлены внутрь — к domain.

---

## Запуск бота через Docker (рекомендуется)

### Шаг 1. Получить токен бота

Открыть Telegram → найти `@BotFather` → `/newbot` → скопировать токен.

### Шаг 2. Заполнить `.env`

```bash
cp .env.example .env
```

Отредактировать `.env` — вставить реальный токен:

```
TELEGRAM_BOT_TOKEN=1234567890:ABCdef...
```

`DATABASE_URL` трогать не нужно — внутри Docker он автоматически переопределяется на `postgres:5432`.

### Шаг 3. Собрать образы

```bash
make build
```

### Шаг 4. Запустить

```bash
make up
```

Postgres поднимется, дождётся healthcheck, затем запустятся миграции (`alembic upgrade head`) и стартует бот.
Написать боту `/start` в Telegram — должен ответить.

### Остановить

```bash
make down
```

---

## Разработка

Все команды запускаются через `make` и выполняются внутри dev-контейнера.
Исходный код монтируется как volume — изменения в файлах видны без пересборки образа.

```bash
make shell      # войти в bash внутри dev-контейнера
make test       # запустить pytest
make lint       # ruff check + ruff format --check + mypy
make lint-fix   # автоисправление ruff
make ci         # полная проверка как в CI (lint + test)
make migrate    # применить миграции вручную (alembic upgrade head)
```

---

## Локальный запуск без Docker

Требуется запущенный PostgreSQL с параметрами из `.env`.

```bash
uv sync --group dev

cp .env.example .env
# Отредактировать .env — добавить TELEGRAM_BOT_TOKEN

uv run alembic upgrade head
uv run python -m interfaces.telegram.bot
```

---

## Первый Admin

После запуска бота назначить себя администратором (Telegram ID можно узнать через `@userinfobot`):

```bash
uv run python scripts/add_admin.py <YOUR_TELEGRAM_ID>
```
