FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код backend
COPY . .

# Устанавливаем PYTHONPATH
ENV PYTHONPATH=/app

# Создаем директорию для статики
RUN mkdir -p static/images
RUN chmod -R 755 static

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
