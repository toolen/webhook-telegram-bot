from unittest.mock import Mock

from aiohttp import web

from repository_telegram_bot.helpers import (
    DATABASE_KEY,
    TELEGRAM_API_KEY,
    TEMPLATE_ENGINE_KEY,
    get_database,
    get_telegram_api,
    get_template_engine,
    set_database,
    set_telegram_api,
    set_template_engine,
)

app = web.Application()


def test_set_database():
    m = Mock()
    set_database(app, m)
    assert app[DATABASE_KEY] is m


def test_get_database():
    m = Mock()
    set_database(app, m)
    assert get_database(app) is m


def test_set_telegram_api():
    m = Mock()
    set_telegram_api(app, m)
    assert app[TELEGRAM_API_KEY] is m


def test_get_telegram_api():
    m = Mock()
    set_telegram_api(app, m)
    assert get_telegram_api(app) is m


def test_set_template_engine():
    m = Mock()
    set_template_engine(app, m)
    assert app[TEMPLATE_ENGINE_KEY] is m


def test_get_template_engine():
    m = Mock()
    set_template_engine(app, m)
    assert get_template_engine(app) is m
