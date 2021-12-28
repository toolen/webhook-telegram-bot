"""This file contains Telegram handlers."""
import json
import logging
from typing import Optional

from aiohttp import web
from aiohttp.web_request import Request

from webhook_telegram_bot.helpers import (
    get_database,
    get_plugins_instances,
    get_telegram_api,
    get_template_engine,
)
from webhook_telegram_bot.telegram.commands import Command
from webhook_telegram_bot.telegram.commands.add_webhook import (
    add_webhook_command_handler,
)
from webhook_telegram_bot.telegram.commands.delete_webhook import (
    delete_webhook_command_handler,
)
from webhook_telegram_bot.telegram.commands.edit_webhook import (
    edit_webhook_command_handler,
)
from webhook_telegram_bot.telegram.commands.edit_webhooks import (
    edit_webhooks_command_handler,
)
from webhook_telegram_bot.telegram.commands.start import start_command_handler

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
    plugins_instances = get_plugins_instances(app)

    text: Optional[str] = telegram_api.get_text(data)
    chat_id: Optional[int] = telegram_api.get_chat_id(data)

    if not text or not chat_id:
        raise Exception()

    if text == Command.START:
        return await start_command_handler(chat_id, db, telegram_api, template_engine)

    elif text == Command.ADD_WEBHOOK:
        plugins_menu_buttons = [
            plugin_instance.get_menu_button() for plugin_instance in plugins_instances
        ]
        return await add_webhook_command_handler(
            chat_id, telegram_api, template_engine, plugins_menu_buttons
        )

    elif text == Command.EDIT_WEBHOOKS:
        return await edit_webhooks_command_handler(
            chat_id, db, telegram_api, template_engine
        )

    elif text.startswith(Command.EDIT_WEBHOOK):
        webhook_id = text.split('_').pop()
        return await edit_webhook_command_handler(
            chat_id, webhook_id, telegram_api, template_engine
        )

    elif text.startswith(Command.DELETE_WEBHOOK):
        webhook_id = text.split('_').pop()
        return await delete_webhook_command_handler(
            chat_id, webhook_id, db, telegram_api, template_engine
        )

    else:

        return await get_response_from_plugins(app, chat_id, text)


async def get_response_from_plugins(
    app: web.Application, chat_id: int, command: str
) -> web.Response:
    """
    Return a response from the plugin if the command refers to one of them.

    :param app:
    :param chat_id:
    :param command:
    :return:
    """
    plugins_instances = get_plugins_instances(app)
    for plugin_instance in plugins_instances:
        resp = plugin_instance.handle_telegram_command(app, chat_id, command)
        if resp:
            return await resp  # type: ignore
    return web.Response()
