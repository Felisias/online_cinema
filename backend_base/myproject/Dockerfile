# 1. Используем официальный образ Python
FROM python:3.11-slim

# 2. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# 3. Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Копируем всё содержимое проекта внутрь контейнера
COPY . .

# 5. Открываем нужный порт
EXPOSE 8000

# 6. Команда по умолчанию: запуск сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
