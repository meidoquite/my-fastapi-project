# FastAPI Todo & ShortURL Services

Два микросервиса на FastAPI с использованием Docker и SQLite.

## Сервисы

1. **ToDo Service** (порт 8000)
   - CRUD операции для задач
   - Документация: http://localhost:8000/docs

2. **ShortURL Service** (порт 8001)
   - Создание коротких ссылок
   - Редирект по короткому ключу
   - Статистика переходов
   - Документация: http://localhost:8001/docs

## Запуск

```bash
# Сборка и запуск контейнеров
docker-compose up --build

# Запуск в фоновом режиме
docker-compose up -d

# Остановка
docker-compose down

# Просмотр логов
docker-compose logs -f