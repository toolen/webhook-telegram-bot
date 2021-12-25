import pytest
from aiohttp import web

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


async def telegram_server_mock_handler(request):
    # bot_token = request.match_info['bot_token']
    command = request.match_info['command']

    if command == 'setWebhook':
        return web.json_response({})


@pytest.fixture
async def telegram_server_mock(aiohttp_server):
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
