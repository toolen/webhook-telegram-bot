"""This file contains functions to handle /bitbucket command."""
import uuid

from aiohttp import web
from jinja2 import Environment

from webhook_telegram_bot.bitbucket.constants import (
    BITBUCKET_TEMPLATE_START,
    BITBUCKET_WEBHOOK_ROUTE,
)
from webhook_telegram_bot.database.backends.types import DatabaseWrapperImpl
from webhook_telegram_bot.database.exceptions import ChatNotFound
from webhook_telegram_bot.database.models import Chat, Service, Webhook
from webhook_telegram_bot.helpers import get_config_value
from webhook_telegram_bot.telegram.commands import Command
from webhook_telegram_bot.telegram.telegram_api import TelegramAPI


async def add_bitbucket_webhook_command_handler(
    app: web.Application,
    chat_id: int,
    db: DatabaseWrapperImpl,
    telegram_api: TelegramAPI,
    template_engine: Environment,
) -> web.Response:
    """
    Return webhook for Bitbucket repository.

    :param app:
    :param chat_id:
    :param db:
    :param telegram_api:
    :param template_engine:
    :return:
    """
    telegram_webhook_host = get_config_value(app, 'TELEGRAM_WEBHOOK_HOST')
    webhook_id: str = uuid.uuid4().hex
    webhook: Webhook = Webhook(webhook_id=webhook_id, service=Service.BITBUCKET)

    try:
        chat = await db.get_chat_by_chat_id(chat_id)
        chat.webhooks.append(webhook)
        await db.save_chat(chat)
    except ChatNotFound:
        chat = Chat(chat_id=chat_id, webhooks=[webhook])
        await db.save_chat(chat)

    template = template_engine.get_template(BITBUCKET_TEMPLATE_START)
    text = template.render(
        webhook_url=f'{telegram_webhook_host}{BITBUCKET_WEBHOOK_ROUTE}/{webhook_id}'
    )

    return telegram_api.send_message_as_response(
        chat_id=chat_id,
        text=text,
        parse_mode='HTML',
        disable_notification=True,
        reply_markup={
            'inline_keyboard': [
                [
                    {
                        'text': '🔙 Back',
                        'callback_data': Command.ADD_WEBHOOK,
                    }
                ]
            ]
        },
    )
