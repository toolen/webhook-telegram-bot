"""This file contains database exception classes."""
from webhook_telegram_bot.exceptions import WebhookBotException


class WebhookAlreadyLinkedToChatException(WebhookBotException):
    """This class represents an exception for the situation when we are trying to add a chat webhook, but it has already been added."""

    pass


class ChatNotFound(WebhookBotException):
    """This class represents an exception for the situation when the chat is not found."""

    pass
