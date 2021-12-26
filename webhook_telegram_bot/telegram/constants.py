"""This file contains telegram module constants."""

import uuid

TELEGRAM_WEBHOOK_TOKEN = uuid.uuid4().hex
TELEGRAM_WEBHOOK_ROUTE = f'/api/v1/telegram/{TELEGRAM_WEBHOOK_TOKEN}'

TELEGRAM_TEMPLATE_START = 'telegram/start.html'
TELEGRAM_TEMPLATE_SELECT_SERVICE = 'telegram/select_service.html'
TELEGRAM_TEMPLATE_EDIT_WEBHOOKS = 'telegram/edit_webhooks.html'
TELEGRAM_TEMPLATE_EDIT_WEBHOOK = 'telegram/edit_webhook.html'
TELEGRAM_TEMPLATE_WEBHOOK_DELETED = 'telegram/webhook_deleted.html'
TELEGRAM_TEMPLATE_CHAT_NOT_FOUND = 'telegram/chat_not_found.html'
