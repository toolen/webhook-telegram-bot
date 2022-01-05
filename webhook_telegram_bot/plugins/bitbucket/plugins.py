"""This file contains implementation of AbstractPlugin."""
from typing import Any, Dict, List, Optional

from aiohttp import web
from jinja2 import PackageLoader

from webhook_telegram_bot.helpers import (
    get_database,
    get_telegram_api,
    get_template_engine,
)
from webhook_telegram_bot.plugins.base import AbstractPlugin
from webhook_telegram_bot.plugins.bitbucket.commands import BitbucketCommand
from webhook_telegram_bot.plugins.bitbucket.commands.add_bitbucket_webhook import (
    add_bitbucket_webhook_command_handler,
)
from webhook_telegram_bot.plugins.bitbucket.routes import init_bitbucket_routes


class Plugin(AbstractPlugin):
    """Implement AbstractPlugin for Bitbucket."""

    def __init__(self, app: web.Application) -> None:
        """
        Construct Plugin object.

        :param app: application instance
        """
        init_bitbucket_routes(app)
        super().__init__(app)

    def get_package_loader(self) -> Dict[str, PackageLoader]:
        """
        Return loader bounded to prefix.

        :return: dict of loaders where each loader is bound to a prefix
        """
        return {'bitbucket': PackageLoader('webhook_telegram_bot.plugins.bitbucket')}

    def is_known_command(self, command: str) -> bool:
        """
        Return True if command refers to a plugin.

        :param command: incoming text from Telegram chat
        :return: True if command refers to a plugin.
        """
        for command_item in BitbucketCommand:
            if command == command_item.value:
                return True
        return False

    async def handle_telegram_command(
        self, app: web.Application, chat_id: int, command: str
    ) -> Optional[web.Response]:
        """
        Handle commands from telegram.

        :param app: application instance
        :param chat_id: chat identification number
        :param command: incoming text from Telegram chat
        :return: bot response
        """
        if command == BitbucketCommand.ADD_BITBUCKET_WEBHOOK:
            telegram_api = get_telegram_api(app)
            db = get_database(app)
            template_engine = get_template_engine(app)
            return await add_bitbucket_webhook_command_handler(
                app, chat_id, db, telegram_api, template_engine
            )
        return None

    def get_menu_button(self) -> List[Dict[str, Any]]:
        """
        Return code for inline keyboard.

        :return: inline keyboard structure
        """
        return [
            {
                'text': 'Bitbucket',
                'callback_data': BitbucketCommand.ADD_BITBUCKET_WEBHOOK,
            }
        ]
