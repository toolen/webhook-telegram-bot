"""This file contains functions to handle /edit_webhook command."""
from aiohttp import web
from jinja2 import Environment

from webhook_telegram_bot.telegram.commands import Command
from webhook_telegram_bot.telegram.telegram_api import TelegramAPI


async def edit_webhook_command_handler(
    chat_id: int,
    webhook_id: str,
    telegram_api: TelegramAPI,
    template_engine: Environment,
) -> web.Response:
    """
    Return list of action with selected webhook.

    :param chat_id:
    :param webhook_id:
    :param telegram_api:
    :param template_engine:
    :return:
    """
    template = template_engine.get_template('edit_webhook.html')
    text = template.render()
    inline_keyboard = [
        [
            {
                'text': '❌ Delete Webhook',
                'callback_data': f'{Command.DELETE_WEBHOOK}_{webhook_id}',
            }
        ],
        [
            {
                'text': '🔙 Back',
                'callback_data': Command.EDIT_WEBHOOKS,
            }
        ],
    ]

    return telegram_api.send_message_as_response(
        chat_id=chat_id,
        text=text,
        parse_mode='HTML',
        disable_notification=True,
        reply_markup={'inline_keyboard': inline_keyboard},
    )
