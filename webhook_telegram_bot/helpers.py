"""This file contains application helpers."""
import importlib
from typing import Any, Dict, List, Optional, Union, cast

from aiohttp import web
from jinja2 import Environment

from webhook_telegram_bot.database.backends.types import DatabaseWrapperImpl
from webhook_telegram_bot.plugins.types import AbstractPluginImpl
from webhook_telegram_bot.telegram.telegram_api import TelegramAPI

CONFIG_KEY = 'CONFIG'
DATABASE_KEY = 'DB'
TELEGRAM_API_KEY = 'TELEGRAM_API'
TEMPLATE_ENGINE_KEY = 'TEMPLATE_ENGINE'
PLUGINS_INSTANCES_KEY = 'PLUGINS_INSTANCES'


def set_config(app: web.Application, config: Dict[str, Any]) -> None:
    """
    Set application config.

    :param app: application instance
    :param config: application configuration
    :return: None
    """
    app[CONFIG_KEY] = config


def get_config(app: web.Application) -> Dict[str, Any]:
    """
    Return application config.

    :param app: application instance
    :return: application configuration
    """
    return cast(Dict[str, Any], app[CONFIG_KEY])


def get_config_value(app: web.Application, key: str) -> Optional[Union[str, List[str]]]:
    """
    Return config value by key.

    :param app: application instance
    :param key: name of config property
    :param key: str
    :return: value of config property
    """
    return get_config(app).get(key)


def set_database(app: web.Application, database: DatabaseWrapperImpl) -> None:
    """
    Set database instance into application.

    :param app: application instance
    :param database: database wrapper instance
    :return: None
    """
    app[DATABASE_KEY] = database


def get_database(app: web.Application) -> DatabaseWrapperImpl:
    """
    Return database instance from application.

    :param app: application instance
    :return: database wrapper instance
    """
    return cast(DatabaseWrapperImpl, app[DATABASE_KEY])


def set_telegram_api(app: web.Application, telegram_api: TelegramAPI) -> None:
    """
    Set TelegramAPI instance into application.

    :param app: application instance
    :param telegram_api: TelegramAPI instance
    :return: None
    """
    app[TELEGRAM_API_KEY] = telegram_api


def get_telegram_api(app: web.Application) -> TelegramAPI:
    """
    Return TelegramAPI instance from application.

    :param app: application instance
    :return: TelegramAPI instance
    """
    return cast(TelegramAPI, app[TELEGRAM_API_KEY])


def set_template_engine(app: web.Application, template_engine: Environment) -> None:
    """
    Set template engine instance into application.

    :param app: application instance
    :param template_engine: instance of template engine
    :return: None
    """
    app[TEMPLATE_ENGINE_KEY] = template_engine


def get_template_engine(app: web.Application) -> Environment:
    """
    Return template engine instance from application.

    :param app: application instance
    :return: instance of template engine
    """
    return cast(Environment, app[TEMPLATE_ENGINE_KEY])


def get_db_wrapper_instance(
    database_engine: str, database_url: str
) -> DatabaseWrapperImpl:
    """
    Return database wrapper instance, according configuration.

    :param database_engine: path to DatabaseWrapper implementation
    :param database_url: connection string to database
    :return: database wrapper instance
    """
    module = importlib.import_module(database_engine)
    db_wrapper_class = getattr(module, 'DatabaseWrapper')
    return cast(DatabaseWrapperImpl, db_wrapper_class(database_url))


def set_plugins_instances(
    app: web.Application, plugins_instances: List[AbstractPluginImpl]
) -> None:
    """
    Set list of plugin instances into application.

    :param app: application instance
    :param plugins_instances: list of plugins instances
    :return: None
    """
    app[PLUGINS_INSTANCES_KEY] = plugins_instances


def get_plugins_instances(app: web.Application) -> List[AbstractPluginImpl]:
    """
    Return list of plugin instances.

    :param app: application instance
    :return: list of plugins instances
    """
    return app.get(PLUGINS_INSTANCES_KEY, [])
