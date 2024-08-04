# syntax=docker/dockerfile:1
FROM python:3.11-alpine
WORKDIR /app
ENV DB_USER=akinon
ENV DB_HOST=host.docker.internal
ENV DB_PORT=5432
ENV BROKER_URL=redis://host.docker.internal:6379/1
ENV CACHE_BACKEND_URL=redis://host.docker.internal:6379/0
RUN apk add gcc musl-dev linux-headers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8887
COPY . .