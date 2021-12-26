"""This file contains types for database layer."""
from typing import Union

from webhook_telegram_bot.database.backends.mongo import (
    DatabaseWrapper as MongoDatabaseWrapper,
)

DatabaseWrapperImpl = Union[MongoDatabaseWrapper]
