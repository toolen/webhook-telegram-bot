FROM python:3.9.9-slim-bullseye@sha256:615ceb9962b182726198d4e71c1b8ecfa4904f83957fb8f4742e573e18e990f7 AS builder

LABEL maintainer="dmitrii@zakharov.cc"
LABEL org.opencontainers.image.source="https://github.com/toolen/webhook-telegram-bot"

ENV \
    DEBIAN_FRONTEND=noninteractive \
    # python:
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip:
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry:
    POETRY_VERSION=1.1.12 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    PATH="$PATH:/root/.local/bin"

RUN pip install --no-cache-dir poetry==$POETRY_VERSION

WORKDIR /code

COPY ./poetry.lock ./pyproject.toml /code/

RUN poetry install --no-dev --no-ansi --no-interaction

COPY ./webhook_telegram_bot /code/webhook_telegram_bot

RUN poetry build --no-ansi --no-interaction

FROM python:3.9.9-alpine3.15@sha256:ce36ba64436cc423fec8b27ac41875e36b0d977cc85594a4cab021ee3378a1c8 AS runner

ENV \
    TIME_ZONE=Europe/Moscow \
    # python:
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip:
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # tini:
    TINI_VERSION=v0.19.0 \
    # gunicorn
    GUNICORN_CMD_ARGS=""

RUN set -ex \
    && apk add --no-cache \
        expat==2.4.3-r0 \
        tini==0.19.0-r0 \
    && addgroup -g 1000 -S app \
    && adduser -h /app -G app -S -u 1000 app

COPY --chown=app:app --from=builder /code/dist/webhook_telegram_bot-*.whl /app

WORKDIR /app

USER app

RUN set -ex \
    && python -m venv venv \
    && venv/bin/pip install --no-cache-dir --target /app/webhook_telegram_bot -- webhook_telegram_bot-*.whl

WORKDIR /app/webhook_telegram_bot

CMD [ "/sbin/tini", "--", "/app/venv/bin/python", "-m", "webhook_telegram_bot.main", "--host", "0.0.0.0", "--port", "8080"]
