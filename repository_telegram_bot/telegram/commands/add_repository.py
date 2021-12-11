"""This file contains functions to handle /add_repository command."""
from aiohttp import web
from jinja2 import Environment

from repository_telegram_bot.telegram.commands import Command
from repository_telegram_bot.telegram.telegram_api import TelegramAPI


async def add_repository_command_handler(
    chat_id: int, telegram_api: TelegramAPI, template_engine: Environment
) -> web.Response:
    """
    Return list of supported services.

    :param chat_id:
    :param telegram_api:
    :param template_engine:
    :return:
    """
    template = template_engine.get_template('select_service.html')
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
                        'callback_data': Command.ADD_BITBUCKET_REPOSITORY,
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
