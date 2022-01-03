"""This file contains abstarct plugin class."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from aiohttp import web
from jinja2 import PackageLoader


class AbstractPlugin(ABC):
    """Abstract class for plugin subclassing."""

    def __init__(self, app: web.Application) -> None:
        """
        Determine constructor signature.

        :param app:
        """
        super().__init__()

    @abstractmethod
    def get_package_loader(self) -> Dict[str, PackageLoader]:
        """
        Return loader bounded to prefix.

        :return:
        """
        pass

    @abstractmethod
    def is_known_command(self, command: str) -> bool:
        """
        Return True if command refers to a plugin.

        :param command:
        :return:
        """
        pass

    @abstractmethod
    async def handle_telegram_command(
        self, app: web.Application, chat_id: int, command: str
    ) -> Optional[web.Response]:
        """
        Abstract method to override.

        :param app:
        :param chat_id:
        :param command:
        :return:
        """
        pass

    @abstractmethod
    def get_menu_button(self) -> List[Dict[str, Any]]:
        """
        Abstract method to override.

        :return:
        """
        pass
