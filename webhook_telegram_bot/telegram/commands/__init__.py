from enum import Enum


class Command(str, Enum):
    """This enum represents bot commands."""

    START = '/start'
    ADD_WEBHOOK = '/add_webhook'
    EDIT_WEBHOOKS = '/edit_webhooks'
    EDIT_WEBHOOK = '/edit_webhook'
    DELETE_WEBHOOK = '/delete_webhook'
