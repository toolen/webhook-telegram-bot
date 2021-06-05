import pytest
from aiohttp import web

from repository_telegram_bot.main import create_app


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
