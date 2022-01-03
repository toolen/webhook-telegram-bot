"""This file contains application exception classes."""


class WebhookBotException(Exception):
    """Base application exception."""

    pass


class ImproperlyConfiguredException(WebhookBotException):
    """Application is somehow improperly configured."""

    pass
