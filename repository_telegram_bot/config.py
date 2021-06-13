"""This file contains config methods."""
import logging
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
        'REDIS_URL': env.get('REDIS_URL', 'redis://localhost:6379'),
        'TEMPLATES_DIR': os.path.join(os.path.dirname(__file__), 'templates'),
        'LOG_LEVEL': logging.getLevelName(env.get('LOG_LEVEL', 'DEBUG')),
    }
