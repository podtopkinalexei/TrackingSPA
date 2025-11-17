FROM python:3.11-slim

WORKDIR /app

# Для Debian-based систем используем этот подход
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Копирование требований
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

RUN useradd -m -r django && chown -R django /app
USER django

EXPOSE 8000
CMD ["gunicorn", "TrackingSPA.wsgi:application", "--bind", "0.0.0.0:8000"]