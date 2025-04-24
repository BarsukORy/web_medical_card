# Используем базовый образ PostgreSQL 16
FROM postgres:16

# Добавляем репозиторий PostgreSQL
RUN echo "deb http://apt.postgresql.org/pub/repos/apt bookworm-pgdg main" > /etc/apt/sources.list.d/pgdg.list

# Устанавливаем необходимые инструменты и расширение pgvector с флагом --allow-unauthenticated
RUN apt-get update && apt-get install -y --allow-unauthenticated \
    postgresql-server-dev-16 \
    gcc \
    make \
    git \
    && git clone https://github.com/pgvector/pgvector.git \
    && cd pgvector \
    && make \
    && make install \
    && cd .. \
    && rm -rf pgvector \
    && apt-get remove -y gcc make git \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Инициализация расширений
RUN echo "CREATE EXTENSION IF NOT EXISTS pg_trgm SCHEMA public;" > /docker-entrypoint-initdb.d/init.sql && \
    echo "CREATE EXTENSION IF NOT EXISTS vector SCHEMA public;" >> /docker-entrypoint-initdb.d/init.sql