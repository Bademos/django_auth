FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка переменных окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Копирование requirements.txt
COPY requirements.txt .

# Установка зависимостей
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Копирование всего проекта
COPY . .

# Создание директорий для статики и медиа
RUN mkdir -p /app/staticfiles /app/media /app/logs

RUN python manage.py collectstatic --noinput

# Создание непривилегированного пользователя
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app


USER appuser

EXPOSE 8000

CMD ["gunicorn", "auth_system.wsgi:application", "--bind", "0.0.0.0:8000"]