FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*
# gcc - это компилятор кода на С так как некоторые библы написаны для питона но не везде на питона и там нужно то что будет компилировать C код -
# ошибки без gcc будут вылезать прямо на этапе pip install
# rm -rf /var/lib/apt/lists/*  уменьшает размер Docker-образа gcc остаётся, удаляется только мусор apt

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

RUN mkdir -p static/images
RUN chmod -R 755 static

EXPOSE 8000
# просто подсказка что контейнер будет работать на этом порту

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
