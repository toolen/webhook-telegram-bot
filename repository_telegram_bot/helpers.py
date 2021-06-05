"""This file contains application helpers."""
from typing import cast

from aiohttp import web
from aioredis import Redis
from jinja2 import Environment

from repository_telegram_bot.telegram.telegram_api import TelegramAPI

DATABASE_KEY = 'DB'
TELEGRAM_API_KEY = 'TELEGRAM_API'
TEMPLATE_ENGINE_KEY = 'TEMPLATE_ENGINE'


def set_database(app: web.Application, database: Redis) -> None:
    """
    Set database instance into application.

    :param app:
    :param database:
    :return:
    """
    app[DATABASE_KEY] = database


def get_database(app: web.Application) -> Redis:
    """
    Return database instance from application.

    :param app:
    :return:
    """
    return app[DATABASE_KEY]


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
