"""This file contains functions to handle /edit_repository command."""
from aiohttp import web
from jinja2 import Environment

from repository_telegram_bot.telegram.commands import Command
from repository_telegram_bot.telegram.telegram_api import TelegramAPI


async def edit_repository_command_handler(
    chat_id: int,
    repository_id: str,
    telegram_api: TelegramAPI,
    template_engine: Environment,
) -> web.Response:
    """
    Return list of action with selected repository.

    :param chat_id:
    :param repository_id:
    :param telegram_api:
    :param template_engine:
    :return:
    """
    template = template_engine.get_template('edit_repository.html')
    text = template.render()
    inline_keyboard = [
        [
            {
                'text': '❌ Delete Repository',
                'callback_data': f'{Command.DELETE_REPOSITORY}_{repository_id}',
            }
        ],
        [
            {
                'text': '🔙 Back',
                'callback_data': Command.EDIT_REPOSITORIES,
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
