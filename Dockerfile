
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
FROM python:3.11-slim


RUN apt-get update && apt-get install -y \
    default-mysql-client \
    libmariadb-dev \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000


