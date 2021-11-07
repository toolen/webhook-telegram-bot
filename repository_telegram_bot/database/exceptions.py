"""This file contains database exception classes."""
from repository_telegram_bot.exceptions import RepositoryBotException


class RepositoryAlreadyLinkedToChatException(RepositoryBotException):
    """This class represents an exception for the situation when we are trying to add a chat repository, but it has already been added."""

    pass


class ChatNotFound(RepositoryBotException):
    """This class represents an exception for the situation when the chat is not found."""

    pass
