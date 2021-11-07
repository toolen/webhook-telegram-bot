"""This file contains types for database layer."""
from typing import Union

from repository_telegram_bot.database.backends.mongo import DatabaseWrapper

DatabaseWrapperImplementation = Union[DatabaseWrapper]
