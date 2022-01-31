"""This file contains application methods."""
import argparse
import importlib
import logging
import ssl
from typing import Dict, Optional, cast

import certifi
from aiohttp import web
from jinja2 import Environment, PackageLoader, PrefixLoader, select_autoescape

from webhook_telegram_bot.config import get_config
from webhook_telegram_bot.exceptions import (
    ImproperlyConfiguredException,
    WebhookBotException,
)
from webhook_telegram_bot.helpers import (
    get_config_value,
    get_database,
    get_db_wrapper_instance,
    get_plugins_instances,
    get_telegram_api,
    set_config,
    set_database,
    set_plugins_instances,
    set_telegram_api,
    set_template_engine,
)
from webhook_telegram_bot.telegram.constants import TELEGRAM_WEBHOOK_ROUTE
from webhook_telegram_bot.telegram.routes import init_telegram_routes
from webhook_telegram_bot.telegram.telegram_api import TelegramAPI

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--host', default="127.0.0.1")
parser.add_argument('--port', default=8080)
parser.add_argument('--ssl', dest='ssl', action='store_true')
parser.set_defaults(ssl=False)


def init_config(
    app: web.Application, override_config: Optional[Dict[str, str]] = None
) -> None:
    """
    Initialize application configuration.

    :param app: application instance
    :param override_config: dictionary that override config
    :return: None
    """
    config = get_config()
    if override_config:
        config.update(override_config)
    set_config(app, config)


def init_logging(app: web.Application) -> None:
    """
    Initialize application logging.

    :param app: application instance
    :return: None
    """
    log_level = cast(str, get_config_value(app, 'LOG_LEVEL'))
    logging.basicConfig(level=log_level)
    logger.debug(f'Logging configured with {log_level} level.')


async def init_database(app: web.Application) -> None:
    """
    Initialize application database.

    :param app: application instance
    :return: None
    """

    async def close_database(app_: web.Application) -> None:
        """
        Close database connection on application shutdown.

        :param app_: application instance
        :return: None
        """
        db_ = get_database(app_)
        db_.close()

    database_url = cast(str, get_config_value(app, 'DATABASE_URL'))
    database_engine = cast(str, get_config_value(app, 'DATABASE_ENGINE'))
    if database_url and database_engine:
        db = get_db_wrapper_instance(database_engine, database_url)
        set_database(app, db)
        app.on_cleanup.append(close_database)
    else:
        raise ImproperlyConfiguredException()


def init_plugins(app: web.Application) -> None:
    """
    Initialize application plugins.

    :param app: application instance
    :return: None
    """
    plugins = get_config_value(app, 'PLUGINS') or []
    plugins_instances = []
    for plugin in plugins:
        module = importlib.import_module(f'{plugin}.plugins')
        if hasattr(module, 'Plugin'):
            plugins_instances.append(module.Plugin(app))
    set_plugins_instances(app, plugins_instances)


def init_templates(app: web.Application) -> None:
    """
    Initialize application template engine.

    :param app: application instance
    :return: None
    """
    prefix_loader_mapping = {
        'telegram': PackageLoader('webhook_telegram_bot.telegram', 'templates'),
    }

    for plugin in get_plugins_instances(app):
        prefix_loader_mapping.update(plugin.get_package_loader())

    template_engine: Environment = Environment(
        loader=PrefixLoader(prefix_loader_mapping),
        autoescape=select_autoescape(['html']),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    set_template_engine(app, template_engine)


def init_telegram(app: web.Application) -> None:
    """
    Initialize Telegram package.

    :param app: application instance
    :return: None
    """

    async def on_startup_telegram_handler(app_: web.Application) -> None:
        telegram_api_endpoint = cast(
            str, get_config_value(app_, 'TELEGRAM_API_ENDPOINT')
        )
        telegram_api_token = cast(str, get_config_value(app_, 'TELEGRAM_API_TOKEN'))

        if not telegram_api_endpoint:
            raise WebhookBotException('TELEGRAM_API_ENDPOINT undefined')

        if not telegram_api_token:
            raise WebhookBotException('TELEGRAM_API_TOKEN undefined')

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


async def create_app(config: Optional[Dict[str, str]] = None) -> web.Application:
    """
    Create application.

    :param config: application configuration
    :return: application instance
    """
    app: web.Application = web.Application()
    init_config(app, config)
    init_logging(app)
    await init_database(app)
    init_plugins(app)
    init_templates(app)
    init_telegram(app)
    return app


def main() -> None:
    """
    Startup application.

    :return: None
    """
    app = create_app()
    args = parser.parse_args()
    ssl_context = (
        ssl.create_default_context(cafile=certifi.where()) if args.ssl else None
    )
    web.run_app(app, host=args.host, port=args.port, ssl_context=ssl_context)


if __name__ == '__main__':
    main()
