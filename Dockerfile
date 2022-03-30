FROM python:3.10.4-slim-bullseye@sha256:3c736db4c8146beb8d04bcb682fd5aec5011d9ff6468f093d4b7e8d2ba8726c7 AS builder

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

RUN poetry export --no-ansi --no-interaction --output requirements.txt

FROM python:3.10.4-alpine3.15@sha256:bd9f7fd93baf921d34f30f585d41081e8a105875ef7de767910659a5f12472e3 AS runner

LABEL maintainer="dmitrii@zakharov.cc"
LABEL org.opencontainers.image.source="https://github.com/toolen/webhook-telegram-bot"

ENV \
    # python:
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip:
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN set -ex \
    && apk upgrade \
    && apk add --no-cache \
        tini==0.19.0-r0 \
    && addgroup -g 1000 -S app \
    && adduser -h /app -G app -S -u 1000 app

COPY --chown=app:app --from=builder /code/requirements.txt /app

WORKDIR /app

USER app

RUN set -ex \
    && python -m venv venv \
    && venv/bin/pip install --no-cache-dir --require-hashes -r requirements.txt

COPY --chown=app:app ./healthcheck.py ./gunicorn.conf.py /app/

COPY --chown=app:app ./webhook_telegram_bot /app/webhook_telegram_bot

EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=10s --retries=3 CMD /app/venv/bin/python healthcheck.py || exit 1

CMD ["/sbin/tini", "--", \
"/app/venv/bin/gunicorn", \
"--config", "/app/gunicorn.conf.py", \
"webhook_telegram_bot.main:create_app"]
