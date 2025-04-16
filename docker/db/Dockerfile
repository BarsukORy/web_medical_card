# Используем базовый образ PostgreSQL 16
FROM postgres:16

# Устанавливаем необходимые инструменты и расширение pgvector
RUN apt-get update && apt-get install -y \
    postgresql-server-dev-16 \
    gcc \
    make \
    git && \
    git clone https://github.com/pgvector/pgvector.git && \
    cd pgvector && \
    make && make install && \
    cd .. && rm -rf pgvector && \
    apt-get remove -y gcc make git && apt-get autoremove -y && apt-get clean

RUN echo "CREATE EXTENSION IF NOT EXISTS pg_trgm SCHEMA public;" > /docker-entrypoint-initdb.d/init.sql && \
    echo "CREATE EXTENSION IF NOT EXISTS vector SCHEMA public;" >> /docker-entrypoint-initdb.d/init.sql