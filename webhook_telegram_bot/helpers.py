"""This file contains application helpers."""
import importlib
from typing import Any, Dict, List, Optional, Union, cast

from aiohttp import web
from jinja2 import Environment, PackageLoader

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

    :param app:
    :param config:
    :return:
    """
    app[CONFIG_KEY] = config


def get_config(app: web.Application) -> Dict[str, Any]:
    """
    Return application config.

    :param app:
    :return:
    """
    return cast(Dict[str, Any], app[CONFIG_KEY])


def get_config_value(app: web.Application, key: str) -> Optional[Union[str, List[str]]]:
    """
    Return config value by key.

    :param app:
    :param key:
    :return:
    """
    return get_config(app).get(key)


def set_database(app: web.Application, database: DatabaseWrapperImpl) -> None:
    """
    Set database instance into application.

    :param app:
    :param database:
    :return:
    """
    app[DATABASE_KEY] = database


def get_database(app: web.Application) -> DatabaseWrapperImpl:
    """
    Return database instance from application.

    :param app:
    :return:
    """
    return cast(DatabaseWrapperImpl, app[DATABASE_KEY])


def set_telegram_api(app: web.Application, telegram_api: TelegramAPI) -> None:
    """
    Set TelegramAPI instance into application.

    :param app:
    :param telegram_api:
    :return:
    """
    app[TELEGRAM_API_KEY] = telegram_api


def get_telegram_api(app: web.Application) -> TelegramAPI:
    """
    Return TelegramAPI instance from application.

    :param app:
    :return:
    """
    return cast(TelegramAPI, app[TELEGRAM_API_KEY])


def set_template_engine(app: web.Application, template_engine: Environment) -> None:
    """
    Set template engine instance into application.

    :param app:
    :param template_engine:
    :return:
    """
    app[TEMPLATE_ENGINE_KEY] = template_engine


def get_template_engine(app: web.Application) -> Environment:
    """
    Return template engine instance from application.

    :param app:
    :return:
    """
    return cast(Environment, app[TEMPLATE_ENGINE_KEY])


def get_db_wrapper_instance(
    database_engine: str, database_url: str
) -> DatabaseWrapperImpl:
    """
    Return database wrapper instance, according configuration.

    :param database_engine:
    :param database_url:
    :return:
    """
    module = importlib.import_module(database_engine)
    db_wrapper_class = getattr(module, 'DatabaseWrapper')
    return cast(DatabaseWrapperImpl, db_wrapper_class(database_url))


def get_prefix_loader_for_plugin(plugin: str) -> Dict[str, PackageLoader]:
    """
    Return arguments from plugin to PrefixLoader.

    :param plugin:
    :return:
    """
    key = plugin.split('.').pop()
    return {key: PackageLoader(plugin, 'templates')}


def set_plugins_instances(
    app: web.Application, plugins_instances: List[AbstractPluginImpl]
) -> None:
    """
    Set list of plugin instances into application.

    :param app:
    :param plugins_instances:
    :return:
    """
    app[PLUGINS_INSTANCES_KEY] = plugins_instances


def get_plugins_instances(app: web.Application) -> List[AbstractPluginImpl]:
    """
    Return list of plugin instances.

    :param app:
    :return:
    """
    return app[PLUGINS_INSTANCES_KEY]
