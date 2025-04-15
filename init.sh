#!/bin/bash

# Ждем, пока база данных будет готова
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database is ready!"

# Применяем миграции
echo "Applying migrations..."
python manage.py migrate

# Собираем статические файлы
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Создаем суперпользователя - администратора
echo "Creating Administrator user..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='Administrator').exists():
    User.objects.create_superuser(
        username='Administrator',
        email='Administrator@aim-cloud.ru',
        password='EBkycuD9|XL%N}Uq',
        full_name='Administrator'
    )
    print('Superuser created successfully')
else:
    print('Superuser already exists')
END
# Создаем суперпользователя - Netology
echo "Creating Netology user..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='netology').exists():
    User.objects.create_superuser(
        username='netology',
        email='netology@aim-cloud.ru',
        password='IUY!#3!rgbtq3w4GB',
        full_name='Netology'
    )
    print('Superuser created successfully')
else:
    print('Superuser already exists')
END

# Запускаем сервер
echo "Starting server..."
exec gunicorn --bind 0.0.0.0:8000 --workers 3 backend.wsgi
# python manage.py runserver 0.0.0.0:8000 