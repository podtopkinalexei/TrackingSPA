FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-dev \
    && rm -rf /var/lib/apt/lists/*

# Копирование требований и установка Python зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

# Создание статических файлов
RUN python manage.py collectstatic --noinput

# Создание пользователя для безопасности
RUN useradd -m -r django && chown -R django /app
USER django

EXPOSE 8000

CMD ["gunicorn", "TrackingSPA.wsgi:application", "--bind", "0.0.0.0:8000"]