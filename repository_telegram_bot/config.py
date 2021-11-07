"""This file contains config methods."""
import os
from typing import Any, Dict

env = os.environ


def get_config() -> Dict[str, Any]:
    """
    Return application config.

    :return:
    """
    return {
        'DEBUG': True,
        'TELEGRAM_API_ENDPOINT': env.get(
            'TELEGRAM_API_ENDPOINT', 'https://api.telegram.org'
        ),
        'TELEGRAM_API_TOKEN': env.get('TELEGRAM_API_TOKEN', ''),
        'TELEGRAM_WEBHOOK_HOST': env.get('TELEGRAM_WEBHOOK_HOST', ''),
        'DATABASE_URL': env.get('DATABASE_URL', 'mongodb://localhost:27017/db'),
        'DATABASE_ENGINE': 'repository_telegram_bot.database.backends.mongo',
        'TEMPLATES_DIR': os.path.join(os.path.dirname(__file__), 'templates'),
        'LOG_LEVEL': env.get('LOG_LEVEL', 'DEBUG'),
    }
