"""This file contains functions to handle /delete_webhook command."""
from aiohttp import web
from jinja2 import Environment

from webhook_telegram_bot.database.backends.types import DatabaseWrapperImpl
from webhook_telegram_bot.database.exceptions import ChatNotFound
from webhook_telegram_bot.database.models import Chat
from webhook_telegram_bot.telegram.commands import Command
from webhook_telegram_bot.telegram.constants import (
    TELEGRAM_TEMPLATE_CHAT_NOT_FOUND,
    TELEGRAM_TEMPLATE_WEBHOOK_DELETED,
)
from webhook_telegram_bot.telegram.telegram_api import TelegramAPI


async def delete_webhook_command_handler(
    chat_id: int,
    webhook_id: str,
    db: DatabaseWrapperImpl,
    telegram_api: TelegramAPI,
    template_engine: Environment,
) -> web.Response:
    """
    Return message about webhook deletion.

    :param chat_id: chat identification number
    :param webhook_id: chat identification string
    :param db: DatabaseWrapper implementation instance
    :param telegram_api: TelegramAPI instance
    :param template_engine: template engine instance
    :return: bot response
    """
    try:
        chat: Chat = await db.get_chat_by_chat_id(chat_id)
        chat.delete_webhook_by_id(webhook_id)
        await db.save_chat(chat)

        template = template_engine.get_template(TELEGRAM_TEMPLATE_WEBHOOK_DELETED)
        text = template.render()
        inline_keyboard = [
            [
                {
                    'text': '🔙 Back',
                    'callback_data': Command.EDIT_WEBHOOKS
                    if len(chat.webhooks)
                    else Command.START,
                }
            ]
        ]
    except ChatNotFound:
        template = template_engine.get_template(TELEGRAM_TEMPLATE_CHAT_NOT_FOUND)
        text = template.render()
        inline_keyboard = [
            [
                {
                    'text': '➕ Add Webhook',
                    'callback_data': Command.ADD_WEBHOOK,
                }
            ]
        ]

    return telegram_api.send_message_as_response(
        chat_id=chat_id,
        text=text,
        parse_mode='HTML',
        disable_notification=True,
        reply_markup={'inline_keyboard': inline_keyboard},
    )
