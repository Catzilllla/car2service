FROM python:3.11-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копируем файлы
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .
COPY rag_services.csv .

CMD ["python", "bot.py"]
