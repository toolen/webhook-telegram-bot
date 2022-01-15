webhook-telegram-bot
=======================
.. image:: https://github.com/toolen/webhook-telegram-bot/actions/workflows/ci.yaml/badge.svg?branch=master
    :target: https://github.com/toolen/webhook-telegram-bot/actions/workflows/ci.yaml
    :alt: CI Status
.. image:: https://coveralls.io/repos/github/toolen/webhook-telegram-bot/badge.svg?branch=master
    :target: https://coveralls.io/github/toolen/webhook-telegram-bot?branch=master
    :alt: Coverage
.. image:: https://readthedocs.org/projects/webhook-telegram-bot/badge/?version=latest
    :target: https://webhook-telegram-bot.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Telegram bot for handling webhooks.

Usage
==========

1. Get token from `BotFather <https://core.telegram.org/bots#6-botfather>`_
2. Setup `MongoDB <https://www.mongodb.com/>`_ or use `container <https://hub.docker.com/_/mongo>`_
3. Run container::

    docker run -d \
    -p 8080:8080 \
    --restart=always \
    --cap-drop=ALL \
    -e "TELEGRAM_API_TOKEN=<token from pt.1>" \
    -e "TELEGRAM_WEBHOOK_HOST=<url where you can access the bot>" \
    -e "DATABASE_URL=<connection string to MongoDB>" \
    ghcr.io/toolen/webhook-telegram-bot:1.0.0

Alternatively, you can use this docker-compose.yml::

    version: "3"
    services:
      bot:
        image: ghcr.io/toolen/webhook-telegram-bot:1.0.0
        restart: always
        ports:
          - "8080:8080"
        environment:
          - "TELEGRAM_API_TOKEN=<token from pt.1>"
          - "TELEGRAM_WEBHOOK_HOST=<url where you can access the bot>"
          - "DATABASE_URL=mongodb://mongo:27017/db"
        cap_drop:
          - ALL
      mongo:
        image: mongo:4.4.9
        container_name: mongo
        hostname: mongo
        restart: always
        volumes:
          - mongo_data:/data/db
    volumes:
      mongo_data:

Settings
==========
Bot can be configured via environment variables:

* TELEGRAM_API_ENDPOINT (default: https://api.telegram.org) - useful if you use your own `Telegram Bot API <https://github.com/tdlib/telegram-bot-api>`_ server or proxy
* TELEGRAM_API_TOKEN - token from `BotFather <https://core.telegram.org/bots#6-botfather>`_
* TELEGRAM_WEBHOOK_HOST - url to receive incoming updates from Telegram API
* DATABASE_URL - url to connect with database (e.g. mongodb://username:password@localhost:27017/db)
* LOG_LEVEL (default: ERROR)

Supported webhooks
======================

Bitbucket
-----------------

Repository events:
 - repo:push
 - repo:commit_comment_created
 - repo:commit_status_updated

Pull request events:
 - pullrequest:created
 - pullrequest:updated
 - pullrequest:approved
 - pullrequest:unapproved
 - pullrequest:fulfilled
 - pullrequest:rejected
 - pullrequest:comment_created
 - pullrequest:comment_updated