"""This file contains application exception classes."""


class WebhookBotException(Exception):
    """Base application exception."""

    pass


class DatabaseUnconfiguredException(WebhookBotException):
    """Exception for unconfigured database."""

    pass
