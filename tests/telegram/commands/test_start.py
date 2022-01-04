import json
from typing import Dict, List
from uuid import uuid4

from first import first

from webhook_telegram_bot.database.models import Chat, Webhook
from webhook_telegram_bot.telegram.commands import Command
from webhook_telegram_bot.telegram.commands.start import start_command_handler
from webhook_telegram_bot.telegram.telegram_api import TelegramAPI

from .utils import get_db_mock, get_template_engine_mock


async def test_start_command_handler_return_add_webhook_button():
    db = get_db_mock()
    telegram_api = TelegramAPI("", "")
    template_engine = get_template_engine_mock()

    resp = await start_command_handler(1, db, telegram_api, template_engine)
    assert resp is not None
    assert resp.status == 200

    data = json.loads(resp.text)
    assert data is not None
    assert 'reply_markup' in data
    assert 'inline_keyboard' in data['reply_markup']
    assert isinstance(data['reply_markup']['inline_keyboard'], List)

    inline_keyboard = data['reply_markup']['inline_keyboard']
    assert len(inline_keyboard) == 1

    inline_keyboard_row = first(inline_keyboard)
    assert isinstance(inline_keyboard_row, List)
    assert len(inline_keyboard_row) == 1

    button = first(inline_keyboard_row)
    assert isinstance(button, Dict)
    assert button['text'] == '➕ Add Webhook'
    assert button['callback_data'] == Command.ADD_WEBHOOK


async def test_start_command_handler_return_edit_webhooks_button():
    webhook_id = uuid4().hex
    chat = Chat(
        id=1,
        chat_id=1,
        webhooks=[Webhook(webhook_id=webhook_id, service='bitbucket')],
    )
    db = get_db_mock(chat)
    telegram_api = TelegramAPI("", "")
    template_engine = get_template_engine_mock()

    resp = await start_command_handler(1, db, telegram_api, template_engine)
    assert resp is not None
    assert resp.status == 200

    data = json.loads(resp.text)
    assert data is not None

    inline_keyboard_row = data['reply_markup']['inline_keyboard']

    assert isinstance(inline_keyboard_row, List)
    assert len(inline_keyboard_row) == 2

    add_webhook_button = inline_keyboard_row[0][0]
    assert isinstance(add_webhook_button, Dict)
    assert add_webhook_button['text'] == '➕ Add Webhook'
    assert add_webhook_button['callback_data'] == Command.ADD_WEBHOOK

    edit_webhooks_button = inline_keyboard_row[1][0]
    assert isinstance(edit_webhooks_button, Dict)
    assert edit_webhooks_button['text'] == '✏ Edit Webhooks'
    assert edit_webhooks_button['callback_data'] == Command.EDIT_WEBHOOKS
