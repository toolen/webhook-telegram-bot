"""This file contains routes of Bitbucket module."""
from aiohttp import web

from webhook_telegram_bot.plugins.bitbucket.constants import BITBUCKET_WEBHOOK_ROUTE
from webhook_telegram_bot.plugins.bitbucket.handlers import bitbucket_webhook_handler


def init_bitbucket_routes(app: web.Application) -> None:
    """
    Initialize Bitbucket module routes.

    :param app:
    :return:
    """
    app.add_routes(
        [
            web.post(
                f'{BITBUCKET_WEBHOOK_ROUTE}/{{webhook_id}}',
                bitbucket_webhook_handler,
                name='bitbucket-webhook',
            )
        ]
    )
