# Используем официальный образ Python 3.11
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Указываем переменные окружения
ENV TELEGRAM_TOKEN=<your_telegram_token>
ENV DB_URL=postgresql+psycopg2://constantine:dox123456@db/numerology_bot

# Запускаем бота
CMD ["python", "main.py"]
