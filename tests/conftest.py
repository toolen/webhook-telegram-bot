from unittest.mock import Mock
from uuid import uuid4

import pytest
from aiohttp import web
from aiohttp.web_request import Request

from webhook_telegram_bot.config import get_config
from webhook_telegram_bot.helpers import get_db_wrapper_instance
from webhook_telegram_bot.main import create_app


@pytest.fixture
def simple_app():
    return web.Application()


@pytest.fixture
async def app():
    app = await create_app()
    return app


@pytest.fixture
async def client(aiohttp_client):
    app = await create_app()
    return await aiohttp_client(app)


@pytest.fixture
async def telegram_server_mock(aiohttp_server):
    async def telegram_server_mock_handler(request: Request):
        # bot_token = request.match_info['bot_token']
        command = request.match_info['command']
        payload = await request.json()
        return web.json_response(
            {'method': request.method, 'command': command, 'payload': payload}
        )

    app = web.Application()
    app.router.add_post('/{bot_token}/{command}', telegram_server_mock_handler)
    server = await aiohttp_server(app)
    return server


@pytest.fixture
async def db_wrapper(loop):
    config = get_config()
    db = get_db_wrapper_instance(config['DATABASE_ENGINE'], config['DATABASE_URL'])
    yield db
    await db.drop_database()
    db.close()


@pytest.fixture
def template_engine_mock():
    template = Mock()
    template.render.return_value = uuid4().hex
    template_engine = Mock()
    template_engine.get_template.return_value = template
    return template_engine
