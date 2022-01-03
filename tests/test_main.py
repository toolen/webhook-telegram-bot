from uuid import uuid4

import pytest
from aiohttp import web
from jinja2 import Environment

from webhook_telegram_bot.config import get_config as get_default_config
from webhook_telegram_bot.database.backends.types import DatabaseWrapperImpl
from webhook_telegram_bot.exceptions import ImproperlyConfiguredException
from webhook_telegram_bot.helpers import (
    get_config,
    get_database,
    get_telegram_api,
    get_template_engine,
)
from webhook_telegram_bot.main import (
    create_app,
    init_config,
    init_database,
    init_logging,
    init_telegram,
    init_templates,
)
from webhook_telegram_bot.telegram.telegram_api import TelegramAPI

app = web.Application()


def test_init_config():
    init_config(app)
    assert get_config(app) == get_default_config()


def test_init_config_with_override():
    override_config = {'TEST': 'TEST'}
    init_config(app, override_config)
    default_config = get_default_config()
    default_config.update(override_config)
    assert get_config(app) == default_config


def test_init_logging(caplog):
    default_config = get_default_config()
    log_level = default_config.get('LOG_LEVEL')
    caplog.set_level(log_level, logger='webhook_telegram_bot.main')
    init_logging(app)
    assert f'Logging configured with {log_level} level.' in caplog.messages


async def test_unconfigured_database():
    test_app = web.Application()
    init_config(
        test_app,
        {
            'DATABASE_URL': None,
        },
    )
    with pytest.raises(ImproperlyConfiguredException):
        await init_database(test_app)
    init_config(test_app, {'DATABASE_ENGINE': None})
    with pytest.raises(ImproperlyConfiguredException):
        await init_database(test_app)
    init_config(test_app, {'DATABASE_URL': None, 'DATABASE_ENGINE': None})
    with pytest.raises(ImproperlyConfiguredException):
        await init_database(test_app)


async def test_init_database():
    await init_database(app)
    db = get_database(app)
    assert isinstance(db, DatabaseWrapperImpl)


async def test_close_database():
    test_app = web.Application()
    init_config(test_app)
    await init_database(test_app)
    test_app.freeze()
    await test_app.startup()
    db = get_database(test_app)
    assert not db.closed

    await test_app.cleanup()
    db = get_database(test_app)
    assert db.closed


def test_init_templates():
    init_templates(app)
    template_engine = get_template_engine(app)
    assert isinstance(template_engine, Environment)


async def test_on_startup_telegram_handler_no_telegram_api_endpoint(aiohttp_server):
    test_app = web.Application()
    init_config(
        test_app,
        {
            'TELEGRAM_API_ENDPOINT': '',
            'TELEGRAM_API_TOKEN': uuid4().hex,
        },
    )
    init_telegram(test_app)
    with pytest.raises(Exception):
        await aiohttp_server(test_app)


async def test_on_startup_telegram_handler_no_telegram_api_token(aiohttp_server):
    test_app = web.Application()
    init_config(
        test_app,
        {
            'TELEGRAM_API_ENDPOINT': 'http://localhost:8080',
            'TELEGRAM_API_TOKEN': '',
        },
    )
    init_telegram(test_app)
    with pytest.raises(Exception):
        await aiohttp_server(test_app)


async def test_on_startup_telegram_handler(aiohttp_server, telegram_server_mock):
    test_app = web.Application()
    init_config(
        test_app,
        {
            'TELEGRAM_API_ENDPOINT': f'http://localhost:{telegram_server_mock.port}',
            'TELEGRAM_API_TOKEN': uuid4().hex,
        },
    )
    init_telegram(test_app)
    await aiohttp_server(test_app)
    telegram_api = get_telegram_api(test_app)
    assert isinstance(telegram_api, TelegramAPI)
    assert telegram_api.active


async def test_on_cleanup_telegram_handler(aiohttp_server, telegram_server_mock):
    test_app = web.Application()
    init_config(
        test_app,
        {
            'TELEGRAM_API_ENDPOINT': f'http://localhost:{telegram_server_mock.port}',
            'TELEGRAM_API_TOKEN': uuid4().hex,
        },
    )
    init_telegram(test_app)
    server = await aiohttp_server(test_app)

    telegram_api = get_telegram_api(test_app)
    assert isinstance(telegram_api, TelegramAPI)

    await server.close()

    assert not telegram_api.active


async def test_create_app(caplog, aiohttp_server, telegram_server_mock):
    default_config = get_default_config()
    log_level = default_config.get('LOG_LEVEL')
    caplog.set_level(log_level, logger='webhook_telegram_bot.main')

    test_app = await create_app(
        {
            'TELEGRAM_API_ENDPOINT': f'http://localhost:{telegram_server_mock.port}',
            'TELEGRAM_API_TOKEN': uuid4().hex,
        }
    )
    server = await aiohttp_server(test_app)

    assert get_config(test_app) is not None
    assert f'Logging configured with {log_level} level.' in caplog.messages
    assert isinstance(get_database(test_app), DatabaseWrapperImpl)
    assert isinstance(get_template_engine(test_app), Environment)
    assert isinstance(get_telegram_api(test_app), TelegramAPI)
    assert test_app.router['bitbucket-webhook'] is not None

    await server.close()
