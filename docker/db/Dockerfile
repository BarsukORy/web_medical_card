# Используем базовый образ PostgreSQL 16
FROM postgres:16

# Устанавливаем ca-certificates и gnupg для работы с HTTPS и GPG-ключами
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Обновляем GPG-ключи для Debian
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 648ACFD622F3D138
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 0E98404D386FA1D9
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 6A7557762E7E2E4A

# Добавляем GPG-ключ для репозитория PostgreSQL и используем HTTPS
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys ACCC4CF8
RUN echo "deb https://ftp.postgresql.org/pub/repos/apt bookworm-pgdg main" > /etc/apt/sources.list.d/pgdg.list

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