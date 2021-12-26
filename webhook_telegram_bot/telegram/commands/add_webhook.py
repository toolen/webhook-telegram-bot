"""This file contains functions to handle /add_webhook command."""
from aiohttp import web
from jinja2 import Environment

from webhook_telegram_bot.bitbucket.commands import BitbucketCommand
from webhook_telegram_bot.telegram.commands import Command
from webhook_telegram_bot.telegram.constants import TELEGRAM_TEMPLATE_SELECT_SERVICE
from webhook_telegram_bot.telegram.telegram_api import TelegramAPI


async def add_webhook_command_handler(
    chat_id: int, telegram_api: TelegramAPI, template_engine: Environment
) -> web.Response:
    """
    Return list of supported services.

    :param chat_id:
    :param telegram_api:
    :param template_engine:
    :return:
    """
    template = template_engine.get_template(TELEGRAM_TEMPLATE_SELECT_SERVICE)
    text = template.render()
    return telegram_api.send_message_as_response(
        chat_id=chat_id,
        text=text,
        parse_mode='HTML',
        disable_notification=True,
        reply_markup={
            'inline_keyboard': [
                [
                    {
                        'text': 'Bitbucket',
                        'callback_data': BitbucketCommand.ADD_BITBUCKET_WEBHOOK,
                    }
                ],
                [
                    {
                        'text': '🔙 Back',
                        'callback_data': Command.START,
                    }
                ],
            ]
        },
    )
