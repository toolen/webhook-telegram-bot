"""This file contains functions to handle /edit_repositories command."""
from aiohttp import web
from jinja2 import Environment

from repository_telegram_bot.database.backends.types import (
    DatabaseWrapperImplementation,
)
from repository_telegram_bot.database.exceptions import ChatNotFound
from repository_telegram_bot.telegram.commands import Command
from repository_telegram_bot.telegram.telegram_api import TelegramAPI


async def edit_repositories_command_handler(
    chat_id: int,
    db: DatabaseWrapperImplementation,
    telegram_api: TelegramAPI,
    template_engine: Environment,
) -> web.Response:
    """
    Return list of repositories associated with the chat.

    :param chat_id:
    :param db:
    :param telegram_api:
    :param template_engine:
    :return:
    """
    try:
        template = template_engine.get_template('edit_repositories.html')
        text = template.render()

        chat = await db.get_chat_by_chat_id(chat_id)
        inline_keyboard = []
        for repository in chat.repositories:
            repository_name = repository.name or repository.repository_id
            inline_keyboard.append(
                [
                    {
                        'text': f'{repository.service}: {repository_name}',
                        'callback_data': f'{Command.EDIT_REPOSITORY}_{repository.repository_id}',
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
        template = template_engine.get_template('chat_not_found.html')
        text = template.render()
        inline_keyboard = [
            [
                {
                    'text': '➕ Add Repository',
                    'callback_data': Command.ADD_REPOSITORY,
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
