"""This file contains Telegram routes."""
from aiohttp import web

from .constants import TELEGRAM_WEBHOOK_ROUTE
from .handlers import telegram_request_handler


def init_telegram_routes(app: web.Application) -> None:
    """
    Initialize Telegram routes.

    :param app:
    :return:
    """
    app.add_routes(
        [
            web.post(
                TELEGRAM_WEBHOOK_ROUTE,
                telegram_request_handler,
                name='telegram-webhook',
            ),
        ]
    )
