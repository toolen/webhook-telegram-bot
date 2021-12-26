"""This file contains types for plugin system."""
from typing import NewType

from webhook_telegram_bot.plugins.base import AbstractPlugin

AbstractPluginImpl = NewType("AbstractPluginImpl", AbstractPlugin)
