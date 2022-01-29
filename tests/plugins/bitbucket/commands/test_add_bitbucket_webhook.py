from uuid import uuid4

from aiohttp import web

from webhook_telegram_bot.helpers import get_telegram_api
from webhook_telegram_bot.main import init_config, init_telegram
from webhook_telegram_bot.plugins.bitbucket.commands.add_bitbucket_webhook import (
    add_bitbucket_webhook_command_handler,
)


async def test_add_bitbucket_webhook_command_handler(
    aiohttp_server, db_wrapper, telegram_server_mock, template_engine_mock
):
    app = web.Application()
    init_config(
        app,
        {
            'TELEGRAM_API_ENDPOINT': f'http://localhost:{telegram_server_mock.port}',
            'TELEGRAM_API_TOKEN': uuid4().hex,
        },
    )
    init_telegram(app)
    chat_id = 1
    await aiohttp_server(app)

    res = await add_bitbucket_webhook_command_handler(
        app, chat_id, db_wrapper, get_telegram_api(app), template_engine_mock
    )
    assert res is not None
