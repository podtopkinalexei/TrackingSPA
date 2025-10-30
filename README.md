```markdown
# Habit Tracker

**Трекер полезных привычек на основе принципов книги "Атомные привычки" Джеймса Клира**

[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14-blue.svg)](https://www.django-rest-framework.org/)
[![Celery](https://img.shields.io/badge/Celery-5.3-darkgreen.svg)](https://docs.celeryq.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-blue.svg)](https://www.postgresql.org/)

## О проекте

Habit Tracker - это веб-приложение для создания и отслеживания полезных привычек, основанное на методологии книги "Атомные привычки". Приложение помогает пользователям формировать новые привычки по принципу: **"Я буду [ДЕЙСТВИЕ] в [ВРЕМЯ] в [МЕСТО]"**.

### 🎯 Ключевые возможности

- Создание полезных и приятных привычек
- Напоминания через Telegram
- Периодическое выполнение привычек
- Система вознаграждений
- Публичные привычки для вдохновения
- REST API для мобильных приложений
- Валидация по принципам "Атомных привычек"

## Быстрый старт

### Предварительные требования

- Python 3.9+
- PostgreSQL 13+
- Redis 6+
- Telegram бот (для уведомлений)

### Установка и запуск

1. **Клонирование репозитория**
```bash
git clone github.com/podtopkinalexei/TrackingSPA
cd habit_tracker
```

2. **Создание виртуального окружения**
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
# или
venv\Scripts\activate  # Windows
```

3. **Установка зависимостей**
```bash
pip install -r requirements.txt
```

4. **Настройка переменных окружения**
```bash
cp .env_temp as example .env
```

5. **Настройка базы данных**
```bash
python manage.py migrate
python manage.py createsuperuser
```

6. **Запуск сервера разработки**
```bash
python manage.py runserver
```

7. **Запуск Celery worker** (в отдельном терминале)
```bash
celery -A config worker -l info
```

8. **Запуск Celery beat** (в отдельном терминале)
```bash
celery -A config beat -l info
```

## Конфигурация

### Основные переменные окружения (.env)

```env
# Безопасность
SECRET_KEY=your-secret-key
DEBUG=True

# База данных
DB_NAME=habit_tracker
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Telegram
TELEGRAM_BOT_TOKEN=your-telegram-bot-token

# CORS
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Создание Telegram бота

1. Найти @BotFather в Telegram
2. Создать нового бота командой `/newbot`
3. Получить токен и добавить в `TELEGRAM_BOT_TOKEN`
4. Получить chat ID пользователя (можно через @userinfobot)
5. Добавить chat ID в профиль пользователя

## Модели данных

### Пользователь (User)
- Стандартные поля Django User
- Telegram Chat ID для уведомлений
- Дополнительные поля профиля

### Привычка (Habit)
```python
{
    "user": "Создатель привычки",
    "place": "Место выполнения",
    "time": "Время выполнения", 
    "action": "Конкретное действие",
    "is_pleasant": "Признак приятной привычки",
    "related_habit": "Связанная приятная привычка",
    "periodicity": "Периодичность (1-7 дней)",
    "reward": "Вознаграждение",
    "time_to_complete": "Время на выполнение (<=120 сек)",
    "is_public": "Публичный доступ"
}
```

## API Endpoints

### Аутентификация
- `POST /api/auth/register/` - Регистрация
- `POST /api/auth/login/` - Вход
- `POST /api/auth/token/refresh/` - Обновление токена
- `GET /api/auth/profile/` - Профиль пользователя

### Привычки
- `GET /api/habits/` - Список привычек пользователя
- `POST /api/habits/` - Создание привычки
- `GET /api/habits/{id}/` - Детали привычки
- `PUT /api/habits/{id}/` - Обновление привычки
- `DELETE /api/habits/{id}/` - Удаление привычки
- `GET /api/habits/public/` - Публичные привычки

## Валидация

Приложение включает строгие валидации согласно принципам "Атомных привычек":

1. **Время выполнения** ≤ 120 секунд
2. **Периодичность** 1-7 дней
3. **Исключено** одновременное указание связанной привычки и вознаграждения
4. **Только приятные привычки** могут быть связанными
5. **У приятных привычек** нет вознаграждений и связанных привычек
6. **Привычки не реже** чем 1 раз в 7 дней


## Интеграция с Telegram

### Настройка уведомлений

1. **Создайте бота** через @BotFather
2. **Получите токен** и настройте в .env
3. **Получите chat ID** пользователя
4. **Добавьте chat ID** в профиль пользователя

### Функциональность

- **Ежеминутные проверки** привычек по времени
- **Автоматические напоминания** в установленное время
- **Детальная информация** о привычке в сообщении
- **Учет периодичности** выполнения


## Тестирование

```bash
# Запуск всех тестов
python manage.py test

# Запуск с покрытием
coverage run manage.py test
coverage report
```

**Требуемое покрытие:** ≥80%

## Технологический стек

### Backend
- **Django 4.2** - Основной фреймворк
- **Django REST Framework** - API
- **PostgreSQL** - База данных
- **Redis** - Брокер для Celery
- **Celery** - Асинхронные задачи
- **Celery Beat** - Периодические задачи

### Безопасность
- **JWT** - Аутентификация
- **CORS** - Межсайтовые запросы
- **Валидаторы** - Бизнес-логика

### Документация
- **DRF Yasg** - Swagger документация
- **Redoc** - Альтернативная документация

## Разработка

### Code Style
- **PEP 8** - Стиль кода Python
- **Django coding style** - Стандарты Django
- **DRF conventions** - Соглашения REST framework

### Коммиты
- **Conventional commits** - Стандартные сообщения
- **English/Russian** - Язык коммитов

## Лицензия

MIT License

