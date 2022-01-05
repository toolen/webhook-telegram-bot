"""This file contains base classes for database layer."""
from abc import ABC, abstractmethod

from webhook_telegram_bot.database.models import Chat


class BaseDatabaseWrapper(ABC):
    """Represent abstract database layer."""

    connection = None
    closed = False

    @abstractmethod
    def __init__(self, url: str):
        """
        Construct BaseDatabaseWrapper subclasses.

        :param url: connection url
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Close database connection.

        :return:
        """
        pass

    @abstractmethod
    async def drop_database(self) -> None:
        """
        Drop database.

        :return:
        """
        pass

    @abstractmethod
    async def get_chat_by_chat_id(self, chat_id: int) -> Chat:
        """
        Return chat by id.

        :param chat_id: chat identification number
        :return:
        """
        pass

    @abstractmethod
    async def get_chat_by_webhook_id(self, webhook_id: str) -> Chat:
        """
        Return chat by webhook id.

        :param webhook_id: webhook identification string
        :return: Chat instance
        """
        pass

    @abstractmethod
    async def save_chat(self, chat: Chat) -> Chat:
        """
        Save chat object to database.

        :param chat: Chat instance
        :return: Chat instance
        """
        pass
