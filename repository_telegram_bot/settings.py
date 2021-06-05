"""This file contains settings methods."""
import logging
import os

env = os.environ

DEBUG = True
TELEGRAM_API_ENDPOINT: str = env.get('TELEGRAM_API_ENDPOINT', 'https://api.telegram.org')
TELEGRAM_API_TOKEN: str = env.get('TELEGRAM_API_TOKEN', '')
TELEGRAM_WEBHOOK_HOST: str = env.get('TELEGRAM_WEBHOOK_HOST')
REDIS_URL = env.get('REDIS_URL', 'redis://localhost:6379')
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')
LOG_LEVEL = logging.getLevelName('DEBUG')
