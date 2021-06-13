"""This file contains application methods."""
import logging
from typing import Dict, Optional

import aioredis
from aiohttp import web
from aioredis import Redis
from jinja2 import Environment, PackageLoader, select_autoescape

from repository_telegram_bot.bitbucket.routes import init_bitbucket_routes
from repository_telegram_bot.config import get_config
from repository_telegram_bot.helpers import (
    get_config_value,
    get_database,
    get_telegram_api,
    set_config,
    set_database,
    set_telegram_api,
    set_template_engine,
)
from repository_telegram_bot.telegram.constants import TELEGRAM_WEBHOOK_ROUTE
from repository_telegram_bot.telegram.routes import init_telegram_routes
from repository_telegram_bot.telegram.telegram_api import TelegramAPI


def init_config(
    app: web.Application, override_config: Optional[Dict[str, str]] = None
) -> None:
    """
    Initialize application configuration.

    :param app:
    :param override_config:
    :return:
    """
    config = get_config()
    if override_config:
        config.update(override_config)
    set_config(app, config)


def init_logging(app: web.Application) -> None:
    """
    Initialize application logging.

    :param app:
    :return:
    """
    log_level = get_config_value(app, 'LOG_LEVEL')
    logging.basicConfig(level=log_level)


async def init_database(app: web.Application) -> None:
    """
    Initialize application database.

    :param app:
    :return:
    """

    async def close_database(app_: web.Application) -> None:
        pool = get_database(app_)
        pool.close()
        await pool.wait_closed()

    redis_url = get_config_value(app, 'REDIS_URL')
    redis_pool: Redis = await aioredis.create_redis_pool(redis_url, encoding="utf-8")
    set_database(app, redis_pool)
    app.on_cleanup.append(close_database)


def init_templates(app: web.Application) -> None:
    """
    Initialize application template engine.

    :param app:
    :return:
    """
    template_engine: Environment = Environment(
        loader=PackageLoader('repository_telegram_bot', 'templates'),
        autoescape=select_autoescape(['html']),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    set_template_engine(app, template_engine)


def init_telegram(app: web.Application) -> None:
    """
    Initialize Telegram package.

    :param app:
    :return:
    """

    async def on_startup_telegram_handler(app_: web.Application) -> None:
        telegram_api_endpoint = get_config_value(app_, 'TELEGRAM_API_ENDPOINT')
        telegram_api_token = get_config_value(app_, 'TELEGRAM_API_TOKEN')

        if not telegram_api_endpoint:
            raise Exception('TELEGRAM_API_ENDPOINT undefined')

        if not telegram_api_token:
            raise Exception('TELEGRAM_API_TOKEN undefined')

        telegram_api = TelegramAPI(
            telegram_api_endpoint,
            telegram_api_token,
            disable_notification=True,
        )

        telegram_webhook_host = get_config_value(app_, 'TELEGRAM_WEBHOOK_HOST')
        telegram_webhook_url = f'{telegram_webhook_host}{TELEGRAM_WEBHOOK_ROUTE}'
        await telegram_api.set_webhook(telegram_webhook_url)
        set_telegram_api(app_, telegram_api)

    async def on_shutdown_telegram_handler(app_: web.Application) -> None:
        telegram_api = get_telegram_api(app_)
        await telegram_api.delete_webhook()

    app.on_startup.append(on_startup_telegram_handler)
    app.on_shutdown.append(on_shutdown_telegram_handler)
    init_telegram_routes(app)


def init_bitbucket(app: web.Application) -> None:
    """
    Initialize Bitbucket package.

    :param app:
    :return:
    """
    init_bitbucket_routes(app)


async def create_app(config: Optional[Dict[str, str]] = None) -> web.Application:
    """
    Create application.

    :return:
    """
    app: web.Application = web.Application()
    init_config(app, config)
    init_logging(app)
    await init_database(app)
    init_templates(app)
    init_telegram(app)
    init_bitbucket(app)
    return app


def main() -> None:
    """
    Startup application.

    :return:
    """
    app = create_app()
    web.run_app(app, host='localhost', port=8080)


if __name__ == '__main__':
    main()
