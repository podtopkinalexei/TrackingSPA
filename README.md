# Habit Tracker

**Трекер полезных привычек на основе принципов книги "Атомные привычки" Джеймса Клира**

## Демо

**Проект развернут на сервере:** `217.197.116.176`

## О проекте

Habit Tracker - это веб-приложение для создания и отслеживания полезных привычек, основанное на методологии книги "Атомные привычки". Приложение помогает пользователям формировать новые привычки по принципу: **"Я буду [ДЕЙСТВИЕ] в [ВРЕМЯ] в [МЕСТО]"**.

### Ключевые возможности

- Создание полезных и приятных привычек
- Напоминания через Telegram
- Периодическое выполнение привычек
- Система вознаграждений
- Публичные привычки для вдохновения
- REST API для мобильных приложений
- Валидация по принципам "Атомных привычек"

## Содержание

- [Быстрый старт](#быстрый-старт)
- [Запуск на сервере](#запуск-на-сервере)
- [CI/CD настройка](#cicd-настройка)
- [Конфигурация](#конфигурация)
- [API документация](#api-документация)
- [Разработка](#разработка)

## Быстрый старт

### Локальная разработка

#### Предварительные требования

- Python 3.9+
- PostgreSQL 13+
- Redis 6+
- Telegram бот (для уведомлений)

#### Установка и запуск

1. **Клонирование репозитория**
```bash
git clone https://github.com/podtopkinalexei/TrackingSPA.git
cd TrackingSPA
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
cp .env.example .env
# Отредактируйте .env файл под вашу конфигурацию
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
celery -A TrackingSPA worker -l info
```

8. **Запуск Celery beat** (в отдельном терминале)
```bash
celery -A TrackingSPA beat -l info
```

### Запуск через Docker (рекомендуется)

1. **Клонирование и настройка**
```bash
git clone https://github.com/podtopkinalexei/TrackingSPA.git
cd TrackingSPA
cp .env.example .env
# Настройте переменные в .env
```

2. **Запуск контейнеров**
```bash
docker-compose up -d
```

3. **Применение миграций**
```bash
docker-compose exec web python manage.py migrate
```

4. **Создание суперпользователя**
```bash
docker-compose exec web python manage.py createsuperuser
```

5. **Сбор статических файлов**
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

Приложение будет доступно по адресу: `http://localhost:80`

## Запуск на сервере

### Подготовка сервера

1. **Установите Docker и Docker Compose на сервер**
```bash
# Для Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl enable docker
sudo systemctl start docker
```

2. **Настройте firewall**
```bash
sudo ufw allow 80
sudo ufw allow 22
sudo ufw enable
```

3. **Клонируйте проект на сервер**
```bash
git clone https://github.com/podtopkinalexei/TrackingSPA.git
cd TrackingSPA
```

4. **Настройте переменные окружения для продакшена**
```bash
cp .env.example .env
nano .env
```

**Важные настройки для продакшена:**
```env
DEBUG=False
SECRET_KEY=your-very-secure-secret-key
ALLOWED_HOSTS=your-domain.com,server-ip
DB_PASSWORD=strong-password
```

5. **Запустите приложение**
```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
docker-compose exec web python manage.py createsuperuser
```

## CI/CD настройка

### GitHub Actions

Проект использует GitHub Actions для автоматического тестирования и деплоя. Конфигурация находится в `.github/workflows/ci-cd.yml`

#### Этапы CI/CD:

1. **Тестирование**
   - Запуск миграций
   - Запуск тестов с SQLite
   - Проверка стиля кода (flake8)
   - Проверка сборки Docker

2. **Сборка**
   - Сборка Docker образов
   - Тестирование контейнеров

3. **Деплой** (только для main ветки)
   - Автоматический деплой на сервер
   - Обновление контейнеров
   - Применение миграций
   - Сбор статических файлов

### Настройка секретов в GitHub

Для работы CI/CD необходимо настроить следующие секреты в репозитории GitHub:

- `SERVER_HOST` - IP адрес сервера
- `SERVER_USER` - пользователь для подключения
- `SERVER_SSH_KEY` - приватный SSH ключ для доступа к серверу
- `DOCKERHUB_USERNAME` - логин Docker Hub (если используется)
- `DOCKERHUB_TOKEN` - токен Docker Hub

### Настройка сервера для CI/CD

1. **Создайте пользователя для деплоя**
```bash
adduser deployer
usermod -aG docker deployer
```

2. **Настройте SSH доступ**
```bash
# На локальной машине
ssh-keygen -t rsa -b 4096 -C "github-actions"
# Скопируйте публичный ключ на сервер
ssh-copy-id deployer@your-server-ip
```

3. **Добавьте приватный ключ в секреты GitHub**

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

# Запуск тестов в Docker
docker-compose exec web python manage.py test
```

## Технологический стек

### Backend
- **Django 4.2** - Основной фреймворк
- **Django REST Framework** - API
- **PostgreSQL** - База данных
- **Redis** - Брокер для Celery
- **Celery** - Асинхронные задачи
- **Celery Beat** - Периодические задачи
- **Docker** - Контейнеризация
- **Nginx** - Веб-сервер

### Безопасность
- **JWT** - Аутентификация
- **CORS** - Межсайтовые запросы
- **Валидаторы** - Бизнес-логика

### Инфраструктура
- **GitHub Actions** - CI/CD
- **Docker Compose** - Оркестрация
- **PostgreSQL** - База данных
- **Redis** - Кэширование и брокер

## Разработка

### Code Style
- **PEP 8** - Стиль кода Python
- **Django coding style** - Стандарты Django
- **DRF conventions** - Соглашения REST framework

### Коммиты
- **Conventional commits** - Стандартные сообщения
- **English/Russian** - Язык коммитов

### Мониторинг

Для проверки статуса сервисов на сервере:
```bash
docker-compose ps
docker-compose logs web
docker-compose logs celery
```

## Лицензия

MIT License
```

### Ключевые дополнения:

1. **Демо** - Добавлен раздел с адресом развернутого приложения
2. **Содержание** - Улучшена навигация по документации
3. **Запуск через Docker** - Добавлены подробные инструкции по контейнеризации
4. **Запуск на сервере** - Полная инструкция по развертыванию на удаленном сервере
5. **CI/CD настройка** - Детальная инструкция по настройке автоматического деплоя
6. **Мониторинг** - Команды для проверки статуса сервисов
7. **Инфраструктура** - Описание используемых технологий для развертывания
