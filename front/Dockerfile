# Stage 1 — сборка проекта
FROM node:20 AS builder

WORKDIR /app
COPY . .
RUN npm install
RUN npm run build

# Stage 2 — запуск с Nginx
FROM nginx:stable-alpine

# Копируем статические файлы
COPY --from=builder /app/dist /usr/share/nginx/html

# Копируем конфиг
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
