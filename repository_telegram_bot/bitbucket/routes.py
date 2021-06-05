"""This file contains routes of Bitbucket module."""
from aiohttp import web

from repository_telegram_bot.settings import DEBUG

from .constants import BITBUCKET_WEBHOOK_ROUTE
from .handlers import bitbucket_debug_template_handler, bitbucket_webhook_handler


def init_bitbucket_routes(app: web.Application) -> None:
    """
    Initialize Bitbucket module routes.

    :param app:
    :return:
    """
    app.add_routes(
        [
            web.post(
                f'{BITBUCKET_WEBHOOK_ROUTE}/{{repository_id}}',
                bitbucket_webhook_handler,
                name='bitbucket-webhook',
            )
        ]
    )
    if DEBUG:
        app.add_routes(
            [
                web.get(
                    f'{BITBUCKET_WEBHOOK_ROUTE}/debug/{{template_name}}',
                    bitbucket_debug_template_handler,
                )
            ]
        )
