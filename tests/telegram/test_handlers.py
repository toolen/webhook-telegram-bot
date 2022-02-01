from unittest.mock import Mock
from uuid import uuid4

from aiohttp import web
from aiohttp.test_utils import make_mocked_request

from webhook_telegram_bot.helpers import set_plugins_instances, set_telegram_api
from webhook_telegram_bot.telegram.commands import Command
from webhook_telegram_bot.telegram.constants import TELEGRAM_WEBHOOK_ROUTE
from webhook_telegram_bot.telegram.handlers import (
    get_response_from_plugins,
    telegram_request_handler,
)
from webhook_telegram_bot.telegram.telegram_api import TelegramAPI


def get_request_with_payload(app, payload):
    async def json_resp():
        return payload

    telegram_api = TelegramAPI("", "")
    set_telegram_api(app, telegram_api)
    request = make_mocked_request('POST', TELEGRAM_WEBHOOK_ROUTE, app=app)
    request.json = json_resp
    return request


async def test_telegram_request_handler_write_log_message_if_no_text(loop, app, caplog):
    get_request_with_payload(app, {'message': {'chat': {'id': 1}}})
    if caplog.messages:
        assert (
            'The message from Telegram does not contain the "text" fields.'
            in caplog.messages
        )


async def test_telegram_request_handler_write_log_message_if_no_chat_id(
    loop, app, caplog
):
    get_request_with_payload(app, {'message': {'text': 'test'}})
    if caplog.messages:
        assert (
            'The message from Telegram does not contain the "chat_id" fields.'
            in caplog.messages
        )


async def test_telegram_request_handler_return_empty_resp_if_command_unknown(loop, app):
    request = get_request_with_payload(
        app, {'message': {'chat': {'id': 1}, 'text': uuid4().hex}}
    )
    resp = await telegram_request_handler(request)
    assert resp is not None
    assert resp.status == 200
    assert resp.body is None


async def test_telegram_request_handler_command_start(loop, app):
    request = get_request_with_payload(
        app, {'message': {'chat': {'id': 1}, 'text': Command.START}}
    )
    resp = await telegram_request_handler(request)
    assert resp is not None
    assert resp.status == 200
    assert resp.body is not None


async def test_telegram_request_handler_command_add_webhook(loop, app):
    request = get_request_with_payload(
        app, {'message': {'chat': {'id': 1}, 'text': Command.ADD_WEBHOOK}}
    )
    resp = await telegram_request_handler(request)
    assert resp is not None
    assert resp.status == 200
    assert resp.body is not None


async def test_telegram_request_handler_command_edit_webhooks(loop, app):
    request = get_request_with_payload(
        app, {'message': {'chat': {'id': 1}, 'text': Command.EDIT_WEBHOOKS}}
    )
    resp = await telegram_request_handler(request)
    assert resp is not None
    assert resp.status == 200
    assert resp.body is not None


async def test_telegram_request_handler_command_edit_webhook(loop, app):
    request = get_request_with_payload(
        app, {'message': {'chat': {'id': 1}, 'text': Command.EDIT_WEBHOOK}}
    )
    resp = await telegram_request_handler(request)
    assert resp is not None
    assert resp.status == 200
    assert resp.body is not None


async def test_telegram_request_handler_command_delete_webhook(loop, app):
    request = get_request_with_payload(
        app, {'message': {'chat': {'id': 1}, 'text': Command.DELETE_WEBHOOK}}
    )
    resp = await telegram_request_handler(request)
    assert resp is not None
    assert resp.status == 200
    assert resp.body is not None


async def test_get_response_from_plugins(loop, app):
    async def handle_telegram_command(app_, chat_id, command):
        return web.json_response({"foo": "bar"})

    plugin = Mock()
    plugin.is_known_command.return_value = True
    plugin.handle_telegram_command = handle_telegram_command

    set_plugins_instances(app, [plugin])

    resp = await get_response_from_plugins(app, 1, 'test')
    assert resp is not None
    assert resp.status == 200
    assert resp.body is not None
