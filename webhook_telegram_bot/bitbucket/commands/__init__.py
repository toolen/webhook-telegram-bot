from enum import Enum


class BitbucketCommand(str, Enum):
    """This enum represents bot commands."""

    ADD_BITBUCKET_WEBHOOK = '/add_bitbucket_webhook'
