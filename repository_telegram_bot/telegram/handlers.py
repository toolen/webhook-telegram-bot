"""This file contains Telegram handlers."""
import json
import logging
from typing import Optional

from aiohttp import web
from aiohttp.web_request import Request

from repository_telegram_bot.helpers import (
    get_database,
    get_telegram_api,
    get_template_engine,
)
from repository_telegram_bot.telegram.commands import Command
from repository_telegram_bot.telegram.commands.add_bitbucket_repository import (
    add_bitbucket_repository_command_handler,
)
from repository_telegram_bot.telegram.commands.add_repository import (
    add_repository_command_handler,
)
from repository_telegram_bot.telegram.commands.delete_repository import (
    delete_repository_command_handler,
)
from repository_telegram_bot.telegram.commands.edit_repositories import (
    edit_repositories_command_handler,
)
from repository_telegram_bot.telegram.commands.edit_repository import (
    edit_repository_command_handler,
)
from repository_telegram_bot.telegram.commands.start import start_command_handler

logger = logging.getLogger(__name__)


async def telegram_request_handler(request: Request) -> web.Response:
    """
    Handle Telegram requests.

    :param request:
    :return:
    """
    data = await request.json()

    logger.debug(f'Request from Telegram: {json.dumps(data)}')

    app = request.app
    telegram_api = get_telegram_api(app)
    db = get_database(app)
    template_engine = get_template_engine(app)

    text: Optional[str] = telegram_api.get_text(data)
    chat_id: Optional[int] = telegram_api.get_chat_id(data)

    if not text or not chat_id:
        raise Exception()

    if text == Command.START:
        return await start_command_handler(chat_id, db, telegram_api, template_engine)

    elif text == Command.ADD_REPOSITORY:
        return await add_repository_command_handler(
            chat_id, telegram_api, template_engine
        )

    elif text == Command.ADD_BITBUCKET_REPOSITORY:
        return await add_bitbucket_repository_command_handler(
            app, chat_id, db, telegram_api, template_engine
        )

    elif text == Command.EDIT_REPOSITORIES:
        return await edit_repositories_command_handler(
            chat_id, db, telegram_api, template_engine
        )

    elif text.startswith(Command.EDIT_REPOSITORY):
        repository_id = text.split('_').pop()
        return await edit_repository_command_handler(
            chat_id, repository_id, telegram_api, template_engine
        )

    elif text.startswith(Command.DELETE_REPOSITORY):
        repository_id = text.split('_').pop()
        return await delete_repository_command_handler(
            chat_id, repository_id, db, telegram_api, template_engine
        )

    else:
        return web.Response()
