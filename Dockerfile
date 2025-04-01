# Используем официальный образ Python 3.12
FROM python:3.12-slim

# Устанавливаем системные зависимости для PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Настройка рабочей директории
WORKDIR /app

# Копируем зависимости первыми для кэширования
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# STATIC_ROOT должна существовать
RUN mkdir -p /app/static

# Копируем весь проект
COPY . .

EXPOSE 8000

# Команда запуска
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "backend.wsgi"]