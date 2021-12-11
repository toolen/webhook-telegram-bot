"""This file contains functions to handle /delete_repository command."""
from aiohttp import web
from jinja2 import Environment

from repository_telegram_bot.database.backends.types import (
    DatabaseWrapperImplementation,
)
from repository_telegram_bot.database.exceptions import ChatNotFound
from repository_telegram_bot.database.models import Chat
from repository_telegram_bot.telegram.commands import Command
from repository_telegram_bot.telegram.telegram_api import TelegramAPI


async def delete_repository_command_handler(
    chat_id: int,
    repository_id: str,
    db: DatabaseWrapperImplementation,
    telegram_api: TelegramAPI,
    template_engine: Environment,
) -> web.Response:
    """
    Return message about repository deletion.

    :param chat_id:
    :param repository_id:
    :param db:
    :param telegram_api:
    :param template_engine:
    :return:
    """
    try:
        chat: Chat = await db.get_chat_by_chat_id(chat_id)
        chat.delete_repository_by_id(repository_id)
        await db.save_chat(chat)

        template = template_engine.get_template('repository_deleted.html')
        text = template.render()
        inline_keyboard = [
            [
                {
                    'text': '🔙 Back',
                    'callback_data': Command.EDIT_REPOSITORIES
                    if len(chat.repositories)
                    else Command.START,
                }
            ]
        ]
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
