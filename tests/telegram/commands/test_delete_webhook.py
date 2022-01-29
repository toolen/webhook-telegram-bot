import json
from typing import Dict, List
from uuid import uuid4

from webhook_telegram_bot.database.models import Chat, Webhook
from webhook_telegram_bot.telegram.commands import Command
from webhook_telegram_bot.telegram.commands.delete_webhook import (
    delete_webhook_command_handler,
)
from webhook_telegram_bot.telegram.telegram_api import TelegramAPI

from .utils import get_db_mock


async def test_delete_webhook_command_handler_return_back_button_if_last_webhook_deleted(
    template_engine_mock,
):
    webhook_id = uuid4().hex
    webhook = Webhook(
        webhook_id=webhook_id, service='bitbucket', repository_name='Test'
    )
    chat = Chat(
        id=1,
        chat_id=1,
        webhooks=[webhook],
    )

    db = get_db_mock(chat)
    telegram_api = TelegramAPI("", "")

    resp = await delete_webhook_command_handler(
        1, webhook_id, db, telegram_api, template_engine_mock
    )
    assert resp is not None
    assert resp.status == 200

    data = json.loads(resp.text)
    assert data is not None

    inline_keyboard_row = data['reply_markup']['inline_keyboard']

    assert isinstance(inline_keyboard_row, List)
    assert len(inline_keyboard_row) == 1

    go_back_button = inline_keyboard_row[0][0]
    assert isinstance(go_back_button, Dict)
    assert go_back_button['text'] == '🔙 Back'
    assert go_back_button['callback_data'] == Command.START


async def test_delete_webhook_command_handler_return_add_webhook_button_if_chat_not_found(
    template_engine_mock,
):
    webhook_id = uuid4().hex
    db = get_db_mock()
    telegram_api = TelegramAPI("", "")

    resp = await delete_webhook_command_handler(
        1, webhook_id, db, telegram_api, template_engine_mock
    )
    assert resp is not None
    assert resp.status == 200

    data = json.loads(resp.text)
    assert data is not None

    inline_keyboard_row = data['reply_markup']['inline_keyboard']

    assert isinstance(inline_keyboard_row, List)
    assert len(inline_keyboard_row) == 1

    go_back_button = inline_keyboard_row[0][0]
    assert isinstance(go_back_button, Dict)
    assert go_back_button['text'] == '➕ Add Webhook'
    assert go_back_button['callback_data'] == Command.ADD_WEBHOOK
