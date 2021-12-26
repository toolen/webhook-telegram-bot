"""This file contains functions to handle /start command."""
from aiohttp import web
from jinja2 import Environment

from webhook_telegram_bot.database.backends.types import DatabaseWrapperImpl
from webhook_telegram_bot.database.exceptions import ChatNotFound
from webhook_telegram_bot.database.models import Chat
from webhook_telegram_bot.telegram.commands import Command
from webhook_telegram_bot.telegram.constants import TELEGRAM_TEMPLATE_START
from webhook_telegram_bot.telegram.telegram_api import TelegramAPI


async def start_command_handler(
    chat_id: int,
    db: DatabaseWrapperImpl,
    telegram_api: TelegramAPI,
    template_engine: Environment,
) -> web.Response:
    """
    Return bot menu.

    :param chat_id:
    :param db:
    :param telegram_api:
    :param template_engine:
    :return:
    """
    template = template_engine.get_template(TELEGRAM_TEMPLATE_START)
    text = template.render()
    inline_keyboard = [
        [
            {
                'text': '➕ Add Webhook',
                'callback_data': Command.ADD_WEBHOOK,
            }
        ]
    ]

    try:
        chat: Chat = await db.get_chat_by_chat_id(chat_id)
        if len(chat.webhooks):
            inline_keyboard.append(
                [
                    {
                        'text': '✏ Edit Webhooks',
                        'callback_data': Command.EDIT_WEBHOOKS,
                    }
                ]
            )
    except ChatNotFound:
        pass

    return telegram_api.send_message_as_response(
        chat_id=chat_id,
        text=text,
        parse_mode='HTML',
        disable_notification=True,
        reply_markup={'inline_keyboard': inline_keyboard},
    )
