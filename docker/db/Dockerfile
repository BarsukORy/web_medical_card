# Используем базовый образ PostgreSQL 16
FROM postgres:16

# Устанавливаем gnupg для работы с GPG-ключами
RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Добавляем GPG-ключ для репозитория PostgreSQL
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 7FCC7D46ACCC4CF8

# Добавляем репозиторий PostgreSQL
RUN echo "deb http://apt.postgresql.org/pub/repos/apt bookworm-pgdg main" > /etc/apt/sources.list.d/pgdg.list

# Устанавливаем необходимые инструменты и расширение pgvector
RUN apt-get update && apt-get install -y \
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