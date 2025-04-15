# Используем официальный образ Python 3.12
FROM python:3.12-slim

# Устанавливаем системные зависимости для PostgreSQL и netcat
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Настройка рабочей директории
WORKDIR /app

# Копируем зависимости первыми для кэширования
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Создаем директорию для статических файлов
RUN mkdir -p /app/static

# Копируем весь проект
COPY . .

# Делаем скрипт инициализации исполняемым
RUN chmod +x init.sh

EXPOSE 8000

# Запускаем скрипт инициализации
CMD ["./init.sh"]