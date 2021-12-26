"""This file contains functions to handle /edit_repositories command."""
from aiohttp import web
from jinja2 import Environment

from webhook_telegram_bot.database.backends.types import DatabaseWrapperImpl
from webhook_telegram_bot.database.exceptions import ChatNotFound
from webhook_telegram_bot.telegram.commands import Command
from webhook_telegram_bot.telegram.constants import (
    TELEGRAM_TEMPLATE_CHAT_NOT_FOUND,
    TELEGRAM_TEMPLATE_EDIT_WEBHOOKS,
)
from webhook_telegram_bot.telegram.telegram_api import TelegramAPI


async def edit_webhooks_command_handler(
    chat_id: int,
    db: DatabaseWrapperImpl,
    telegram_api: TelegramAPI,
    template_engine: Environment,
) -> web.Response:
    """
    Return list of webhooks associated with the chat.

    :param chat_id:
    :param db:
    :param telegram_api:
    :param template_engine:
    :return:
    """
    try:
        template = template_engine.get_template(TELEGRAM_TEMPLATE_EDIT_WEBHOOKS)
        text = template.render()

        chat = await db.get_chat_by_chat_id(chat_id)
        inline_keyboard = []
        for webhook in chat.webhooks:
            repository_name = webhook.repository_name or webhook.webhook_id
            inline_keyboard.append(
                [
                    {
                        'text': f'{webhook.service}: {repository_name}',
                        'callback_data': f'{Command.EDIT_WEBHOOK}_{webhook.webhook_id}',
                    }
                ]
            )
        inline_keyboard.append(
            [
                {
                    'text': '🔙 Back',
                    'callback_data': Command.START,
                }
            ]
        )

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
