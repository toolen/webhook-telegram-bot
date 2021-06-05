"""This file contains telegram module constants."""

import uuid

from repository_telegram_bot.settings import TELEGRAM_WEBHOOK_HOST

TELEGRAM_WEBHOOK_TOKEN = uuid.uuid4().hex
TELEGRAM_WEBHOOK_ROUTE = f'/api/v1/telegram/{TELEGRAM_WEBHOOK_TOKEN}'
TELEGRAM_WEBHOOK_URL = f'{TELEGRAM_WEBHOOK_HOST}{TELEGRAM_WEBHOOK_ROUTE}'
