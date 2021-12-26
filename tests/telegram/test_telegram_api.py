import json
from uuid import uuid4

from aiohttp import web

from webhook_telegram_bot.telegram.telegram_api import TelegramAPI

telegram_api = TelegramAPI("", "")


def test_get_chat_id_from_message():
    chat_id = 1
    returned_chat_id = telegram_api.get_chat_id({"message": {"chat": {"id": chat_id}}})
    assert chat_id == returned_chat_id


def test_get_chat_id_from_callback_query():
    chat_id = 1
    returned_chat_id = telegram_api.get_chat_id(
        {"callback_query": {"message": {"chat": {"id": chat_id}}}}
    )
    assert chat_id == returned_chat_id


def test_get_text_from_message():
    text = uuid4().hex
    returned_text = telegram_api.get_text({"message": {"text": text}})
    assert text == returned_text


def test_get_text_from_callback_query():
    text = uuid4().hex
    returned_text = telegram_api.get_text({"callback_query": {"data": text}})
    assert text == returned_text


def test_send_message_as_response():
    resp = telegram_api.send_message_as_response(foo="bar")
    data = json.loads(resp.body)
    assert resp is not None
    assert isinstance(resp, web.Response)
    assert 'method' in data
    assert data['method'] == 'sendMessage'
    assert 'foo' in data
    assert data['foo'] == 'bar'
