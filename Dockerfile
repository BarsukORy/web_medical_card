# Базовый образ с Docker CLI и Alpine
FROM docker:24.0.2-cli

# Устанавливаем docker-compose и bash
RUN apk add --no-cache docker-compose bash

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем весь проект внутрь контейнера
COPY . .

# Команда запуска: поднимаем весь стек
CMD ["sh", "-c", "docker-compose up"]
