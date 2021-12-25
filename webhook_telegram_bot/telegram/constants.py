"""This file contains telegram module constants."""

import uuid

TELEGRAM_WEBHOOK_TOKEN = uuid.uuid4().hex
TELEGRAM_WEBHOOK_ROUTE = f'/api/v1/telegram/{TELEGRAM_WEBHOOK_TOKEN}'
